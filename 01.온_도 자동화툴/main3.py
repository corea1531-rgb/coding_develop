import sys
import difflib
from pathlib import Path
import requests
import pandas as pd
from create_file import save_files_vba_compatible

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox, QDialog,
    QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit
)
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem

from send_invoice import run_send_invoice
from autotool_ui import Ui_MainWindow

# ✅ collectors.py 쪽에 구현되어 있어야 함:
# - collect_all_by_accounts(logger, accounts) -> (onch_path, df_dm)
from collectors import collect_all_by_accounts


# =========================
# 전역 - 롯데택배 파일 컬럼
# =========================
LOTTE_EXPECTED_HEADERS = [
    'NO','작업구분','작업구분상세명','합포장여부','합포장순번','합포장키','운송장번호','이전운송장번호','자료등록일','주문번호',
    '쇼핑몰','출력여부','관리번호','주문자명','고정수하인코드','수하인명','수하인기본주소','송하인명','송하인기본주소',
    'A','B','C','D','E','F',
    '운임구분','집하일자','집하점소','상품명','상품코드','상품상세내용','상품옵션명','상품스타일명','최초지시일자','원운송장번호',
    '특기사항','출고구분','터미널명','집배센터명','내품개수','고객메세지','기본운임','연계비용','배송점소명','배송지구분',
    '상품가','집하사원','배달주기'
]

# =========================
# 수령인 검수 로직(전역)
# =========================
COL_A_NAME = 0        # A열: 이름
COL_C_PLATFORM = 2    # C열: 플랫폼명
COL_D_PRODUCT = 3     # D열: 제품코드
COL_K_ORDERNO = 10    # K열: 주문코드


def _clean_series(s: pd.Series) -> pd.Series:
    return s.astype(str).replace("nan", "").str.strip()


def check_merge_forbidden(excel_path: str) -> pd.DataFrame:
    """
    수령인 검수:
    - (이름 A, 제품코드 D) 그룹에서 주문코드 K가 2개 이상이면 "확인 필요"
    반환: 문제 행들 DataFrame (표시용: 이름(A), 플랫폼명(C), 주문코드(K))
    """
    df = pd.read_excel(excel_path, header=None, dtype=str)

    if df.shape[1] <= COL_K_ORDERNO:
        raise ValueError(f"엑셀 열 개수가 부족합니다. 현재 {df.shape[1]}열인데 K열(11번째 열)이 필요합니다.")

    a = _clean_series(df.iloc[:, COL_A_NAME])
    c = _clean_series(df.iloc[:, COL_C_PLATFORM])
    d = _clean_series(df.iloc[:, COL_D_PRODUCT])
    k = _clean_series(df.iloc[:, COL_K_ORDERNO])

    work = pd.DataFrame({
        "이름(A)": a,
        "플랫폼명(C)": c,
        "제품코드(D)": d,
        "주문코드(K)": k,
    })

    valid = (work["이름(A)"] != "") & (work["제품코드(D)"] != "") & (work["주문코드(K)"] != "")
    work = work[valid].copy()

    if work.empty:
        return work.iloc[0:0]

    k_nunique = work.groupby(["이름(A)", "제품코드(D)"])["주문코드(K)"].transform("nunique")
    bad = work[k_nunique >= 2].copy()
    bad.sort_values(["이름(A)", "제품코드(D)", "주문코드(K)"], inplace=True)

    return bad[["이름(A)", "플랫폼명(C)", "주문코드(K)"]].copy()


# =========================
# 실재고 검수 로직(전역)
# =========================
NEEDED_COLS = ["수취인명", "상품명", "옵션명", "샵플링 매핑옵션코드", "주문수량", "실재고", "자사코드"]


def load_and_check_stock(excel_path: str):
    df = pd.read_excel(excel_path, dtype=str)

    missing = [c for c in NEEDED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"엑셀에 필요한 컬럼이 없습니다: {missing}")

    for c in NEEDED_COLS:
        df[c] = df[c].astype(str).replace("nan", "").str.strip()

    df["주문수량_num"] = pd.to_numeric(df["주문수량"], errors="coerce").fillna(0).astype(int)
    df["실재고_num"] = pd.to_numeric(df["실재고"], errors="coerce").fillna(0).astype(int)

    df["유효"] = (
        (df["수취인명"] != "") &
        (df["샵플링 매핑옵션코드"] != "") &
        (df["샵플링 매핑옵션코드"] != "0")
    )

    df["총주문수량"] = 0
    df.loc[df["유효"], "총주문수량"] = (
        df.loc[df["유효"]]
        .groupby("샵플링 매핑옵션코드")["주문수량_num"]
        .transform("sum")
        .astype(int)
    )

    df["결과값"] = ""
    df.loc[df["유효"], "결과값"] = df.loc[df["유효"]].apply(
        lambda r: "출고 가능" if r["실재고_num"] >= r["총주문수량"] else "재고 부족",
        axis=1
    )

    df_lack = df[(df["유효"]) & (df["결과값"] == "재고 부족")].copy()
    show_cols = ["수취인명", "상품명", "옵션명", "주문수량", "실재고", "자사코드"]
    df_lack_show = df_lack[show_cols].copy()

    return df, df_lack_show


# ==================
# 라이선스 검증 스레드
# ==================
class LicenseWorker(QThread):
    finished = Signal(bool, str)   # ok, reason

    def __init__(self, fn_verify, code: str, parent=None):
        super().__init__(parent)
        self.fn_verify = fn_verify
        self.code = code

    def run(self):
        ok, reason = self.fn_verify(self.code)
        self.finished.emit(ok, reason)


# ==================
# 송장 전송 스레드
# ==================
class SendInvoiceWorker(QThread):
    log_signal = Signal(str)
    done_signal = Signal()
    error_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def log(self, msg: str):
        self.log_signal.emit(msg)

    def run(self):
        try:
            self.log("=== 송장 전송 시작 ===")
            run_send_invoice(logger=self.log)
            self.log("=== 송장 전송 완료 ===")
            self.done_signal.emit()
        except Exception as e:
            self.error_signal.emit(str(e))


# =========================
# 주문수집 스레드 (accounts.json 기반)
# =========================
class CollectorWorker(QThread):
    log_signal = Signal(str)
    done_signal = Signal()
    error_signal = Signal(str)
    free_shipping_signal = Signal(list)   # ✅ 추가

    def __init__(self, accounts: dict, parent=None):
        super().__init__(parent)
        self.accounts = accounts

    def log(self, msg: str):
        self.log_signal.emit(msg)

    def run(self):
        try:
            self.log("=== 수집 시작 ===")

            onch_path, df_dm = collect_all_by_accounts(logger=self.log, accounts=self.accounts)

            # ---- 온채널 표시
            try:
                df_on = pd.read_excel(onch_path, dtype=str).fillna("")
            except Exception as e:
                self.log(f"❌ 온채널 병합파일 읽기 실패: {e}")
                df_on = pd.DataFrame()

            if len(df_on) > 0 and df_on.shape[1] >= 10:
                self.log("온채널 병합 파일 내역 표시:")
                for _, r in df_on.iterrows():
                    cust = str(r.iloc[8]).strip()
                    prod = str(r.iloc[2]).strip()
                    opt = str(r.iloc[4]).strip()
                    qty = str(r.iloc[5]).strip()
                    self.log(f"- {cust} | {prod} | {opt} | {qty}")

                phones = df_on.iloc[:, 9].astype(str).str.strip()
                phones = phones[phones.ne("")]
                unique_cnt = int(phones.nunique())
                self.log(f"✅ 온채널 {unique_cnt}건 주문수집 완료")

                # ✅ 무료배송 검사 (H열=7번 인덱스, A/C/E/I = 0/2/4/8)
                if df_on.shape[1] >= 9:
                    h_col = df_on.iloc[:, 7].astype(str).str.strip()
                    free_df = df_on[h_col.eq("무료배송")].copy()

                    if not free_df.empty:
                        free_rows = []
                        for _, r in free_df.iterrows():
                            a_val = str(r.iloc[0]).strip() if len(r) > 0 else ""
                            c_val = str(r.iloc[2]).strip() if len(r) > 2 else ""
                            e_val = str(r.iloc[4]).strip() if len(r) > 4 else ""
                            i_val = str(r.iloc[8]).strip() if len(r) > 8 else ""
                            free_rows.append((a_val, c_val, e_val, i_val))

                        self.free_shipping_signal.emit(free_rows)

            else:
                self.log("✅ 온채널 0건 주문수집 완료")

            # ---- 도매의신 표시
            if df_dm is None:
                df_dm = pd.DataFrame()

            if len(df_dm) > 0:
                self.log("도매의신 수집 내역 표시:")
                dff = df_dm.fillna("")
                for _, r in dff.iterrows():
                    receiver = str(r.get("수취인", "")).strip()
                    product_name = str(r.get("상품명", "")).strip()
                    option_name = str(r.get("선택옵션", "")).strip()
                    quantity = str(r.get("수량", "")).strip()
                    self.log(f"- {receiver} | {product_name} | {option_name} | {quantity}")

                receivers = dff["수취인"].astype(str).str.strip()
                receivers = receivers[receivers.ne("")]
                unique_cnt = int(receivers.nunique())
                self.log(f"✅ 도매의신 {unique_cnt}건 주문수집 완료")
            else:
                self.log("✅ 도매의신 0건 주문수집 완료")

            self.log("=== 전체 수집 완료 ===")
            self.done_signal.emit()

        except Exception as e:
            self.error_signal.emit(str(e))


# ==================
# 팝업 다이얼로그
# ==================
class HoldContinueDialog(QDialog):
    """보류: 닫지 않고 멈춤 / 계속: accept()로 닫고 진행"""
    def __init__(self, parent=None, message=""):
        super().__init__(parent)
        self.setWindowTitle("확인 필요")
        self.setModal(True)
        self.setMinimumWidth(560)

        self.label = QLabel(message)
        self.label.setWordWrap(True)

        self.hold_btn = QPushButton("보류")
        self.continue_btn = QPushButton("계속")

        self.hold_btn.clicked.connect(self.on_hold)
        self.continue_btn.clicked.connect(self.accept)

        btns = QHBoxLayout()
        btns.addStretch(1)
        btns.addWidget(self.hold_btn)
        btns.addWidget(self.continue_btn)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addLayout(btns)

    def on_hold(self):
        if "[보류중]" not in self.label.text():
            self.label.setText(self.label.text() + "\n\n[보류중] 확인 후 '계속'을 눌러 진행하세요.")
        self.hold_btn.setEnabled(False)


# =========================
# 메인 윈도우
# =========================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # ✅ UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("케이엠_온채널&도매의신 자동화툴")

        # ✅ 라이선스 서버 설정 (중복 금지: 여기서 1번만!)
        self.LICENSE_URL = "https://script.google.com/macros/s/AKfycbwQ8hu-OslOB74MNEkzYA2tyDV7ptmw6dQbG0IkhG1ZcI5NwgyShr60xpD1blYsSw0Qow/exec"
        self.LICENSE_API_KEY = "KMTRADE_SECRET_2026"

        # ✅ 이 PC 고유값(승인/차단용) - 1번만!
        self.device_id = self.get_device_hash()

        # ✅ 로그인 코드 캐시용
        self.last_login_code = ""

        # ✅ accounts.json 로드/생성
        self.accounts = self.load_accounts_json_local()

        # ✅ 처음 화면: 로그인
        self.ui.stacked_main.setCurrentWidget(self.ui.page_login)

        # ✅ 테마 적용
        self.apply_dark_theme()

        # ✅ 로그인 입력칸: **** 표시
        self.ui.code_name.setEchoMode(QLineEdit.Password)
        self.ui.code_name.setPlaceholderText("코드를 입력하세요")

        # 주문검수(page_check) 세팅
        self.setup_page_check()

        # 주문수집 로그(listView)
        self.view_model = QStandardItemModel(self.ui.listView)
        self.ui.listView.setModel(self.view_model)

        # 송장(page_invoice) - send_list 모델
        self.lotte_path = None  # 롯데택배 업로드 파일 경로
        self.send_model = QStandardItemModel(self.ui.send_list)
        self.ui.send_list.setModel(self.send_model)

        # 스레드
        self.worker = None
        self.send_worker = None
        self.lic_worker = None

        # 버튼 연결 (메인)
        self.ui.order_collect_btn.clicked.connect(self.go_page_collect)
        self.ui.order_check_btn.clicked.connect(self.go_page_check)
        self.ui.invoice_send_btn.clicked.connect(self.go_page_invoice)

        # 뒤로가기
        self.ui.Back_btn1.clicked.connect(self.go_page_main)
        self.ui.Back_btn2.clicked.connect(self.on_click_back_btn2)
        self.ui.Back_btn3.clicked.connect(self.on_click_back_btn3)

        # 주문수집 시작 버튼
        self.ui.start_order_btn.clicked.connect(self.start_collectors)

        # 송장전송 버튼
        self.ui.send_invoice_btn.clicked.connect(self.on_click_send_invoice)

        # 롯데 업로드 / 등록파일 생성
        self.ui.lotte_upload_btn.clicked.connect(self.upload_lotte_file)
        self.ui.creat_file_btn.clicked.connect(self.on_click_create_files)

        # ✅ 로그인 버튼
        self.ui.login_btn.clicked.connect(self.on_click_login)
        self.ui.code_name.returnPressed.connect(self.on_click_login)  # 엔터로 로그인

    # =========================
    # PC 고유값 (승인/차단용)
    # =========================
    def get_device_hash(self) -> str:
        import hashlib
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
            guid, _ = winreg.QueryValueEx(key, "MachineGuid")
            raw = f"MachineGuid:{guid}".encode("utf-8")
        except Exception:
            import socket
            raw = f"Host:{socket.gethostname()}".encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    # =========================
    # 라이선스 캐시(60분) + 자동 재검증
    # =========================
    def _license_cache_path(self) -> Path:
        import os
        base = Path(os.path.dirname(sys.executable)) if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
        return base / "license_cache.json"

    def _load_license_cache(self) -> dict:
        import json
        p = self._license_cache_path()
        if not p.exists():
            return {}
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _save_license_cache(self, data: dict) -> None:
        import json
        p = self._license_cache_path()
        try:
            p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

    def is_license_recent_ok(self, ttl_seconds: int = 3600) -> bool:
        import time
        cache = self._load_license_cache()
        last_ok = cache.get("last_ok_ts")
        if not isinstance(last_ok, (int, float)):
            return False
        return (time.time() - float(last_ok)) <= ttl_seconds

    def mark_license_ok_now(self) -> None:
        import time
        self._save_license_cache({"last_ok_ts": time.time()})

    def _lock_ui_for_license_check(self, lock: bool, hint: str = "확인 중..."):
        """라이선스 확인 중 중복 클릭 방지용(필요한 버튼들만 잠금)"""
        # 로그인 UI
        if hasattr(self.ui, "login_btn"):
            self.ui.login_btn.setEnabled(not lock)
            self.ui.login_btn.setText(hint if lock else "로그인")
        if hasattr(self.ui, "code_name"):
            self.ui.code_name.setEnabled(not lock)

        # 메인 기능 버튼들(있는 것만)
        for name in [
            "start_order_btn", "send_invoice_btn", "creat_file_btn",
            "lotte_upload_btn",
            "order_collect_btn", "order_check_btn", "invoice_send_btn",
            "stock_btn", "costomer_btn"
        ]:
            if hasattr(self.ui, name):
                try:
                    getattr(self.ui, name).setEnabled(not lock)
                except Exception:
                    pass

    def ensure_license_then(self, callback, ttl_seconds: int = 3600):
        """
        - 최근 ttl_seconds 이내 OK면 즉시 callback 실행
        - 만료면 백그라운드로 서버 재검증 후 OK면 callback 실행
        - 실패면 로그인 페이지로 이동
        """
        if self.is_license_recent_ok(ttl_seconds=ttl_seconds):
            callback()
            return

        self._lock_ui_for_license_check(True, "확인 중...")

        code = (self.last_login_code or "").strip()
        if not code:
            self._lock_ui_for_license_check(False)
            QMessageBox.information(self, "인증 필요", "라이선스 확인이 필요합니다.\n로그인 코드를 입력해 주세요.")
            self.go_page_login()
            self.ui.code_name.setFocus()
            return

        self.lic_worker = LicenseWorker(self.verify_login_code_online, code, self)

        def _done(ok: bool, reason: str):
            self._lock_ui_for_license_check(False)

            if ok:
                self.mark_license_ok_now()
                callback()
                return

            # 실패 처리
            if reason.startswith("network_error"):
                msg = "인터넷 연결을 확인해 주세요.\n(라이선스 서버 확인 실패)"
            elif reason == "device_pending":
                msg = "이 PC는 아직 승인되지 않았습니다.\n관리자 승인 후 다시 로그인하세요."
            elif reason == "device_blocked":
                msg = "이 PC는 차단되었습니다.\n관리자에게 문의하세요."
            elif reason == "inactive":
                msg = "이 코드는 비활성화되었습니다.\n관리자에게 문의하세요."
            elif reason == "not_found":
                msg = "코드가 올바르지 않습니다.\n다시 입력해 주세요."
            elif reason == "invalid_api_key":
                msg = "프로그램 인증키가 올바르지 않습니다.\n(개발자 설정 오류)"
            else:
                msg = f"인증 실패: {reason}"

            QMessageBox.warning(self, "인증 필요", msg)
            self.go_page_login()
            self.ui.code_name.setFocus()
            self.ui.code_name.selectAll()

        self.lic_worker.finished.connect(_done)
        self.lic_worker.start()

    def verify_login_code_online(self, code: str) -> tuple[bool, str]:
        """
        반환:
        - (True, "")                : 인증 성공
        - (False, "inactive")       : 비활성 코드
        - (False, "not_found")      : 코드 없음
        - (False, "device_pending") : PC 승인 대기
        - (False, "device_blocked") : PC 차단
        - (False, "invalid_api_key"): API 키 불일치
        - (False, "network_error: ...") : 네트워크/서버/파싱 등 예외
        """
        import json

        try:
            r = requests.post(
                self.LICENSE_URL,
                json={
                    "code": code,
                    "api_key": self.LICENSE_API_KEY,
                    "device": self.device_id
                },
                headers={"Content-Type": "application/json"},
                timeout=10
            )
        except Exception as e:
            return False, f"network_error: request_failed: {type(e).__name__}: {e}"

        try:
            data = r.json()
        except Exception:
            try:
                data = json.loads(r.text)
            except Exception:
                preview = (r.text or "")[:200].replace("\n", " ")
                return False, f"network_error: bad_response: HTTP {r.status_code} | {preview}"

        if data.get("ok") is True:
            return True, ""

        return False, str(data.get("reason", "invalid"))

    # -------------------------
    # accounts.json
    # -------------------------
    def load_accounts_json_local(self) -> dict:
        import json

        if getattr(sys, "frozen", False):
            base_dir = Path(sys.executable).resolve().parent
        else:
            base_dir = Path(__file__).resolve().parent

        user_json = base_dir / "accounts.json"

        bundled_json = None
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            cand = Path(sys._MEIPASS) / "accounts.json"
            if cand.exists():
                bundled_json = cand

        if not user_json.exists():
            if bundled_json and bundled_json.exists():
                user_json.write_text(bundled_json.read_text(encoding="utf-8"), encoding="utf-8")
            else:
                default = {
                    "onchannel": {"sm": {"id": "", "pw": ""}, "km": {"id": "", "pw": ""}},
                    "domesin": {"id": "", "pw": ""},
                    "ownerclan": {"id": "", "pw": ""}
                }
                user_json.write_text(json.dumps(default, ensure_ascii=False, indent=2), encoding="utf-8")
                return default

        return json.loads(user_json.read_text(encoding="utf-8"))

    # -------------------------
    # 테마
    # -------------------------
    def apply_dark_theme(self):
        APP_QSS = r"""
        QWidget {
            background-color: #2B2B2B;
            color: #F2F2F2;
            font-size: 13pt;
        }
        QLabel { color: #F2F2F2; }

        QLineEdit {
            background-color: #3A3A3A;
            color: #FFFFFF;
            border: 1px solid #555555;
            border-radius: 10px;
            padding: 8px 10px;
        }

        QPushButton {
            background-color: #3D3D3D;
            color: #FFFFFF;
            border: 1px solid #5A5A5A;
            border-radius: 12px;
            padding: 10px 14px;
            font-weight: 600;
        }
        QPushButton:hover { background-color: #4A4A4A; }
        QPushButton:pressed { background-color: #353535; }
        QPushButton:disabled {
            background-color: #2F2F2F;
            color: #9A9A9A;
            border: 1px solid #3B3B3B;
        }

        #code {
            font-size: 24pt;
            font-weight: 800;
        }

        QListView {
            background-color: #505050;
            color: #FFFFFF;
            border: 1px solid #6A6A6A;
            border-radius: 12px;
            padding: 10px;
            outline: none;
        }
        QListView::item { padding: 10px 10px; border-radius: 10px; }
        QListView::item:hover { background-color: #5E5E5E; }
        QListView::item:selected { background-color: #7A7A7A; color: #FFFFFF; }
        """
        self.setStyleSheet(APP_QSS)

    # -------------------------
    # 로그인
    # -------------------------
    def on_click_login(self):
        code = self.ui.code_name.text().strip()

        if not code:
            QMessageBox.warning(self, "로그인 실패", "코드를 입력해 주세요.")
            self.ui.code_name.setFocus()
            return

        self.ui.login_btn.setEnabled(False)
        self.ui.code_name.setEnabled(False)
        self.ui.login_btn.setText("확인 중...")

        self.lic_worker = LicenseWorker(self.verify_login_code_online, code, self)
        self.lic_worker.finished.connect(self._on_license_done)
        self.lic_worker.start()

    def _on_license_done(self, ok: bool, reason: str):
        self.ui.login_btn.setEnabled(True)
        self.ui.code_name.setEnabled(True)
        self.ui.login_btn.setText("로그인")

        if ok:
            self.last_login_code = self.ui.code_name.text().strip()
            self.mark_license_ok_now()
            self.ui.code_name.clear()
            self.go_page_main()
            return

        if reason.startswith("network_error"):
            msg = "인터넷 연결을 확인해 주세요.\n(라이선스 서버 확인 실패)"
        elif reason == "device_pending":
            msg = "이 PC는 아직 승인되지 않았습니다.\n관리자 승인 후 다시 로그인하세요."
        elif reason == "device_blocked":
            msg = "이 PC는 차단되었습니다.\n관리자에게 문의하세요."
        elif reason == "inactive":
            msg = "이 코드는 비활성화되었습니다.\n관리자에게 문의하세요."
        elif reason == "not_found":
            msg = "코드가 올바르지 않습니다.\n다시 입력해 주세요."
        elif reason == "invalid_api_key":
            msg = "프로그램 인증키가 올바르지 않습니다.\n(개발자 설정 오류)"
        else:
            msg = f"로그인 실패: {reason}"

        QMessageBox.warning(self, "로그인 실패", msg)
        self.ui.code_name.setFocus()
        self.ui.code_name.selectAll()

    # -------------------------
    # 페이지 이동
    # -------------------------
    def go_page_invoice(self):
        self.ui.stacked_main.setCurrentWidget(self.ui.page_invoice)

    def go_page_main(self):
        self.ui.stacked_main.setCurrentWidget(self.ui.page_main)

    def go_page_collect(self):
        self.ui.stacked_main.setCurrentWidget(self.ui.page_collect)

    def go_page_check(self):
        self.ui.stacked_main.setCurrentWidget(self.ui.page_check)

    def go_page_login(self):
        self.resize(780, 620)
        self.ui.stacked_main.setCurrentWidget(self.ui.page_login)

    # -------------------------
    # 송장(page_invoice) 상태 초기화
    # -------------------------
    def reset_invoice_state(self):
        self.lotte_path = None
        self.send_model.clear()

    def on_click_back_btn3(self):
        if self.send_worker and self.send_worker.isRunning():
            self.add_send("⚠️ 송장 전송이 진행 중입니다. 완료 후 뒤로가기를 권장합니다.")

        self.reset_invoice_state()
        self.go_page_main()

    # -------------------------
    # 송장 전송(스레드)
    # -------------------------
    def on_click_send_invoice(self):
        def _go():
            downloads = Path.home() / "Downloads"
            if not (downloads / "온채널 송장등록.xlsx").exists():
                self.add_send("❌ 온채널 송장등록.xlsx 없음 (등록파일 생성부터 해주세요)")
                return

            if self.send_worker and self.send_worker.isRunning():
                self.add_send("이미 송장 전송이 진행 중입니다.")
                return

            self.ui.send_invoice_btn.setEnabled(False)
            self.add_send("⏳ 송장 전송 중...")

            self.send_worker = SendInvoiceWorker(self)
            self.send_worker.log_signal.connect(self.add_send)
            self.send_worker.done_signal.connect(self.on_send_done)
            self.send_worker.error_signal.connect(self.on_send_error)
            self.send_worker.start()

        self.ensure_license_then(_go, ttl_seconds=3600)

    def on_send_done(self):
        self.add_send("✅ 송장 전송 스레드 종료")
        self.ui.send_invoice_btn.setEnabled(True)

    def on_send_error(self, err: str):
        self.add_send(f"❌ 송장 전송 오류: {err}")
        self.ui.send_invoice_btn.setEnabled(True)

    # -------------------------
    # 공용 로그
    # -------------------------
    def add_send(self, msg: str):
        self.send_model.appendRow(QStandardItem(msg))
        self.ui.send_list.scrollToBottom()
        QApplication.processEvents()

    def append_view(self, msg: str):
        self.view_model.appendRow(QStandardItem(msg))
        self.ui.listView.scrollToBottom()
        QApplication.processEvents()

    # -------------------------
    # 온채널 무료배송 확인
    # -------------------------


    def on_free_shipping_found(self, free_rows: list):
        if not free_rows:
            return

        self.append_view("⚠️ 온채널 무료배송 주문건 확인")
        for a_val, c_val, e_val, i_val in free_rows:
            self.append_view(f"{a_val} | {c_val} | {e_val} | {i_val}")

        QMessageBox.information(
            self,
            "확인",
            "온채널 주문건 중 무료배송 주문건이 확인되었습니다",
            QMessageBox.Ok
        )

    # -------------------------
    # 등록파일 생성 버튼
    # -------------------------
    def on_click_create_files(self):
        def _go():
            ok = self.check_onchannel_jeju_by_aq()
            if not ok:
                return
            self.add_send("✅ (검수 통과) 등록파일 생성을 시작합니다.")
            self.run_pidpic_create_files()

        self.ensure_license_then(_go, ttl_seconds=3600)

    def run_pidpic_create_files(self):
        if not self.lotte_path:
            QMessageBox.warning(self, "파일 필요", "롯데택배 파일을 먼저 업로드 해주세요.")
            return

        try:
            self.add_send("⏳ 등록파일 생성 중...")

            shoppling, onchannel, domesin = save_files_vba_compatible(Path(self.lotte_path))

            self.add_send("✅ 샵플링 송장등록.xlsx 생성")
            self.add_send("✅ 온채널 송장등록.xlsx 생성")
            if domesin:
                self.add_send("✅ 도매의신 송장등록.xls 생성")
            else:
                self.add_send("ℹ️ 도매의신 주문 없음(파일 생성 안 함)")

            QMessageBox.information(self, "완료", "등록파일 3개 생성 완료")
            return

        except Exception as e:
            QMessageBox.critical(self, "실패", f"등록파일 생성 실패\n{e}")
            self.add_send(f"❌ 등록파일 생성 실패: {e}")
            return

    # -------------------------
    # 롯데 업로드 검증/업로드
    # -------------------------
    def validate_lotte_file(self, excel_path: str) -> None:
        try:
            df0 = pd.read_excel(excel_path, nrows=0)
        except Exception as e:
            raise ValueError(f"엑셀을 읽을 수 없습니다: {e}")

        headers = [str(c).strip() for c in df0.columns.tolist()]

        if headers != LOTTE_EXPECTED_HEADERS:
            diff = "\n".join(difflib.unified_diff(
                LOTTE_EXPECTED_HEADERS, headers,
                fromfile="EXPECTED", tofile="UPLOADED", lineterm=""
            ))
            raise ValueError("롯데택배 업로드 양식 헤더가 다릅니다.\n" + diff)

    def get_downloads_path(self) -> Path:
        return Path.home() / "Downloads"

    def upload_lotte_file(self):
        start_dir = str(self.get_downloads_path())
        path, _ = QFileDialog.getOpenFileName(
            self, "롯데택배 파일 업로드", start_dir, "Excel Files (*.xlsx *.xls)"
        )
        if not path:
            return

        try:
            self.validate_lotte_file(path)
        except Exception as e:
            self.lotte_path = None
            QMessageBox.warning(self, "업로드 파일 확인", f"업로드 파일을 확인해 주세요\n\n{e}", QMessageBox.Ok)
            self.add_send(f"❌ 롯데택배 파일 오류: {e}")
            return

        self.lotte_path = path
        self.add_send("✅ 롯데택배 파일 업로드 완료")

    def check_onchannel_jeju_by_aq(self) -> bool:
        if not self.lotte_path:
            QMessageBox.information(self, "업로드 필요", "롯데택배 파일을 먼저 업로드 해주세요.", QMessageBox.Ok)
            return False

        try:
            df = pd.read_excel(self.lotte_path, dtype=str).fillna("")
        except Exception as e:
            QMessageBox.warning(self, "오류", f"엑셀을 읽을 수 없습니다.\n{e}", QMessageBox.Ok)
            return False

        required = ["쇼핑몰", "연계비용", "수하인명", "수하인기본주소"]
        missing = [c for c in required if c not in df.columns]
        if missing:
            QMessageBox.warning(self, "업로드 파일 확인", "업로드 파일을 확인해 주세요", QMessageBox.Ok)
            self.add_send("❌ 롯데택배 파일 오류")
            self.lotte_path = None
            return False

        shop = df["쇼핑몰"].astype(str).str.strip()
        aq = pd.to_numeric(df["연계비용"], errors="coerce").fillna(0)
        mask = (shop == "온채널") & (aq > 1000)

        if not mask.any():
            self.add_send("온채널 제주지역 0건")
            return True

        target = df.loc[mask, ["수하인명", "쇼핑몰", "수하인기본주소"]].copy()

        self.add_send("⚠️ 온채널 제주/도서산간 의심 건 확인 필요")
        for _, r in target.iterrows():
            p = str(r.get("수하인명", "")).strip()
            k = str(r.get("쇼핑몰", "")).strip()
            q = str(r.get("수하인기본주소", "")).strip()
            self.add_send(f"{p} | {k} | {q}")

        dlg = HoldContinueDialog(
            self,
            "온채널 주문건에서 제주 또는 도서산간 주소지가 확인 되었습니다.\n계속 진행 하시겠습니까?"
        )
        dlg.exec()
        return True

    # -------------------------
    # 주문수집
    # -------------------------
    def start_collectors(self):
        def _go():
            if self.worker and self.worker.isRunning():
                self.append_view("이미 수집이 진행 중입니다.")
                return

            self.view_model.clear()
            self.ui.start_order_btn.setEnabled(False)

            self.worker = CollectorWorker(self.accounts, self)
            self.worker.log_signal.connect(self.append_view)
            self.worker.done_signal.connect(self.on_done)
            self.worker.error_signal.connect(self.on_error)
            self.worker.free_shipping_signal.connect(self.on_free_shipping_found)   # ✅ 추가
            self.worker.start()

        self.ensure_license_then(_go, ttl_seconds=3600)

    def on_done(self):
        self.append_view("✅ 수집 스레드 종료")
        self.ui.start_order_btn.setEnabled(True)

    def on_error(self, err: str):
        self.append_view(f"❌ 오류: {err}")
        self.ui.start_order_btn.setEnabled(True)

    # =========================
    # 주문검수(page_check)
    # =========================
    def setup_page_check(self):
        self.stock_path = None
        self.customer_path = None
        self.stock_checked_after_both_upload = False

        self.status_lines = []
        self.result_lines = []

        self.check_model = QStandardItemModel(self.ui.check_list)
        self.ui.check_list.setModel(self.check_model)
        self.render_check_list()

        self.ui.stock_file.clicked.connect(self.upload_stock_file)
        self.ui.customer_file.clicked.connect(self.upload_customer_file)
        self.ui.stock_btn.clicked.connect(self.on_click_stock_check)
        self.ui.costomer_btn.clicked.connect(self.on_click_customer_check)

    def render_check_list(self):
        self.check_model.clear()
        for s in self.status_lines:
            self.check_model.appendRow(QStandardItem(s))
        for s in self.result_lines:
            self.check_model.appendRow(QStandardItem(s))

    def reset_check_vars_only(self):
        self.stock_path = None
        self.customer_path = None
        self.stock_checked_after_both_upload = False

    def reset_check_all_for_new_upload(self):
        self.result_lines = []

    def add_result(self, text: str):
        self.result_lines.append(text)
        self.render_check_list()

    def popup_ok(self, title: str, msg: str):
        QMessageBox.information(self, title, msg, QMessageBox.Ok)

    def popup_confirm_or_continue(self, title: str, msg: str) -> bool:
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Warning)
        box.setWindowTitle(title)
        box.setText(msg)

        btn_ok = box.addButton("확인", QMessageBox.RejectRole)
        btn_continue = box.addButton("계속", QMessageBox.AcceptRole)
        box.setDefaultButton(btn_continue)

        box.exec()
        return box.clickedButton() == btn_continue

    def safe_save_excel_noheader(self, df: pd.DataFrame, out_path: Path) -> Path:
        try:
            df.to_excel(out_path, index=False, header=False)
            return out_path
        except PermissionError:
            ts = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
            new_path = out_path.with_stem(out_path.stem + f"_{ts}")
            df.to_excel(new_path, index=False, header=False)
            return new_path

    def push_status_line(self, kind: str, filename: str):
        prefix = "실재고 검수파일 업로드" if kind == "stock" else "수령인 검수파일 업로드"
        newline = f"✅ {prefix}: {filename}"

        def is_same_kind(s: str) -> bool:
            return (kind == "stock" and "실재고 검수파일 업로드" in s) or \
                   (kind == "customer" and "수령인 검수파일 업로드" in s)

        self.status_lines = [s for s in self.status_lines if not is_same_kind(s)]
        self.status_lines.append(newline)
        if len(self.status_lines) > 2:
            self.status_lines = self.status_lines[-2:]

    def upload_stock_file(self):
        start_dir = str(self.get_downloads_path())
        path, _ = QFileDialog.getOpenFileName(
            self, "실재고 검수파일 업로드", start_dir, "Excel Files (*.xlsx *.xls)"
        )
        if not path:
            return

        self.reset_check_all_for_new_upload()
        self.stock_path = path
        self.stock_checked_after_both_upload = False

        self.push_status_line("stock", Path(path).name)
        self.render_check_list()

    def upload_customer_file(self):
        start_dir = str(self.get_downloads_path())
        path, _ = QFileDialog.getOpenFileName(
            self, "수령인 검수파일 업로드", start_dir, "Excel Files (*.xlsx *.xls)"
        )
        if not path:
            return

        self.reset_check_all_for_new_upload()
        self.customer_path = path
        self.stock_checked_after_both_upload = False

        self.push_status_line("customer", Path(path).name)
        self.render_check_list()

    def require_file(self, path, msg: str) -> bool:
        if not path:
            self.popup_ok("업로드 필요", msg)
            return False
        return True

    def validate_a_column_match(self) -> bool:
        if not (self.stock_path and self.customer_path):
            return True

        try:
            df_stock = pd.read_excel(self.stock_path)
            df_cust = pd.read_excel(self.customer_path, header=None)
        except Exception as e:
            self.reset_check_all_for_new_upload()
            self.render_check_list()
            self.add_result("파일 오류")
            self.popup_ok("오류", f"엑셀을 읽을 수 없습니다.\n{e}")
            return False

        stock_a = df_stock.iloc[:, 0].astype(str).replace("nan", "").str.strip()
        cust_a = df_cust.iloc[:, 0].astype(str).replace("nan", "").str.strip()

        stock_a = stock_a[stock_a.ne("")]
        cust_a = cust_a[cust_a.ne("")]

        if sorted(stock_a.tolist()) != sorted(cust_a.tolist()):
            self.reset_check_all_for_new_upload()
            self.render_check_list()
            self.add_result("파일 오류")
            self.popup_ok("검수 파일 확인 바랍니다", "검수 파일 확인 바랍니다")
            return False

        return True

    def on_click_stock_check(self):
        if not self.require_file(self.stock_path, "실재고 검수파일(stock_file)을 먼저 업로드 해주세요."):
            return

        if not self.validate_a_column_match():
            return

        self.result_lines = []
        self.render_check_list()

        if self.stock_path and self.customer_path:
            self.stock_checked_after_both_upload = True

        try:
            _, df_lack = load_and_check_stock(self.stock_path)
        except Exception:
            self.add_result("파일 오류")
            self.popup_ok("검수 파일 확인 바랍니다", "검수 파일 확인 바랍니다")
            return

        if df_lack.empty:
            self.add_result("실재고 검수 이상 없음")
            return

        for _, r in df_lack.fillna("").iterrows():
            self.add_result(
                f"{r['수취인명']} | {r['상품명']} | {r['옵션명']} | 주문:{r['주문수량']} | 재고:{r['실재고']} | 코드:{r['자사코드']}"
            )

    def on_click_customer_check(self):
        if not self.require_file(self.customer_path, "수령인 검수파일(customer_file)을 먼저 업로드 해주세요."):
            return

        if self.stock_path and self.customer_path and not self.stock_checked_after_both_upload:
            self.popup_ok("순서 필요", "두 파일을 업로드한 경우, 실재고 검수를 먼저 진행해주세요.")
            return

        if not self.validate_a_column_match():
            return

        self.result_lines = []
        self.render_check_list()

        try:
            bad_df = check_merge_forbidden(self.customer_path)
        except Exception as e:
            self.add_result("파일 오류")
            self.popup_ok("검수 파일 확인 바랍니다", f"검수 파일 확인 바랍니다\n\n{e}")
            return

        if bad_df.empty:
            self.add_result("수령인 검수 이상 없음")
            try:
                df_cust = pd.read_excel(self.customer_path, header=None)
                out_path = self.get_downloads_path() / "롯데택배 업로드 파일.xlsx"
                saved = self.safe_save_excel_noheader(df_cust, out_path)
                self.add_result(f"✅ 저장 완료: {saved.name}")
                self.reset_check_vars_only()
                return
            except Exception as e:
                self.popup_ok("저장 오류", f"엑셀 저장 중 오류:\n{e}")
                return

        for _, r in bad_df.fillna("").iterrows():
            self.add_result(f"{r['이름(A)']} | {r['플랫폼명(C)']} | {r['주문코드(K)']}")

        go_on = self.popup_confirm_or_continue(
            "수령인 확인 필요",
            "동일한 수령인과 동일한 상품코드에서\n"
            "서로 다른 주문코드가 함께 존재합니다.\n\n"
            "합포장이 가능한 주문인지\n"
            "반드시 확인이 필요합니다.\n\n"
            "계속 진행하면 송장 업로드 파일이 생성됩니다."
        )
        if not go_on:
            return

        try:
            df_cust = pd.read_excel(self.customer_path, header=None)
            out_path = self.get_downloads_path() / "롯데택배 업로드 파일.xlsx"
            saved = self.safe_save_excel_noheader(df_cust, out_path)
            self.add_result(f"✅ 저장 완료: {saved.name}")
            self.reset_check_vars_only()
            return
        except Exception as e:
            self.popup_ok("저장 오류", f"엑셀 저장 중 오류:\n{e}")
            return

    def on_click_back_btn2(self):
        self.stock_path = None
        self.customer_path = None
        self.stock_checked_after_both_upload = False
        self.status_lines = []
        self.result_lines = []
        self.render_check_list()
        self.go_page_main()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())