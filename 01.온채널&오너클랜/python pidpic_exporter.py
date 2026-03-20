import sys
from pathlib import Path

import pandas as pd
import xlwings as xw
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QMessageBox, QLineEdit
)

DOWNLOADS = Path.home() / "Downloads"
DOMESIN_KEYWORD = "도매의신"


# -----------------------------
# PIDPIC -> 3개 출력 데이터 만들기
# -----------------------------
def build_outputs(pidpic_path: Path):
    df = pd.read_excel(pidpic_path, dtype=str)

    # NaN/공백 정리
    df = df.fillna("")
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    required = ["주문번호", "쇼핑몰", "운송장번호", "수하인명", "상품상세내용"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"PIDPIC 파일에 필요한 컬럼이 없습니다: {missing}")

    # 1) 샵플링(Sheet1): 상품상세내용이 비어있지 않은 행
    lot = df[df["상품상세내용"] != ""].copy()
    sheet1_out = pd.DataFrame({
        "A": lot["상품상세내용"],
        "B": lot["운송장번호"],
        "C": ["050"] * len(lot),
    })

    # 2) 온채널: 주문번호 prefix MO/GO
    order_prefix = df["주문번호"].str[:2]
    on = df[order_prefix.isin(["MO", "GO"])].copy()
    on_out = pd.DataFrame({
        "주문코드": on["주문번호"],
        "택배사": ["35"] * len(on),
        "송장번호": on["운송장번호"],
    })

    # 3) 도매의신: 쇼핑몰 == 도매의신
    dom = df[df["쇼핑몰"] == DOMESIN_KEYWORD].copy()
    dom_out = pd.DataFrame({
        "주문번호": dom["주문번호"],
        "택배업체코드": ["10"] * len(dom),
        "송장번호": dom["운송장번호"],
        "수취인명": dom["수하인명"],
    })

    return sheet1_out, on_out, dom_out


# -----------------------------
# 저장 함수 (VBA와 동일 파일명)
# -----------------------------
def save_shoppling_xlsx(sheet1_out: pd.DataFrame, out_path: Path):
    # VBA: Sheet1.UsedRange 값을 새 통합문서에 저장
    # 파이썬: 동일하게 값만 저장(헤더 없음)
    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        sheet1_out.to_excel(writer, sheet_name="Sheet1", index=False, header=False)


def save_onchannel_xlsx(on_out: pd.DataFrame, out_path: Path):
    # VBA: 온채널 시트에서 lastRow까지 "행 전체" 값 복사
    # 파이썬: on_out 전체를 값으로 저장(헤더 포함)
    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        on_out.to_excel(writer, sheet_name="Sheet1", index=False)


def save_domesin_xls_with_xlwings(dom_out: pd.DataFrame, out_path: Path):
    app = xw.App(visible=False, add_book=False)
    app.display_alerts = False
    app.screen_updating = False
    wb = None
    try:
        wb = app.books.add()
        ws = wb.sheets[0]
        ws.name = "Sheet1"

        # ✅ (추가1) A열(주문번호)을 텍스트로 고정
        ws.range("A:A").api.NumberFormat = "@"

        # 헤더 포함 저장
        data = [dom_out.columns.tolist()] + dom_out.astype(str).values.tolist()
        ws.range("A1").value = data

        # ✅ (추가2) 헤더 제외 A열 주문번호만 한번 더 확정(엑셀 자동 숫자변환 방지)
        last_row = len(dom_out) + 1
        ws.range(f"A2:A{last_row}").value = [[v] for v in dom_out["주문번호"].astype(str).tolist()]

        wb.api.SaveAs(str(out_path), FileFormat=56)
    finally:
        try:
            if wb:
                wb.close()
        except:
            pass
        app.quit()


def save_files_vba_compatible(pidpic_path: Path):
    sheet1_out, on_out, dom_out = build_outputs(pidpic_path)

    # VBA와 동일 파일명(다운로드 폴더 고정, 덮어쓰기)
    shoppling_path = DOWNLOADS / "샵플링 송장등록.xlsx"
    onchannel_path = DOWNLOADS / "온채널 송장등록.xlsx"
    domesin_path   = DOWNLOADS / "도매의신 송장등록.xls"

    # 1) 샵플링
    save_shoppling_xlsx(sheet1_out, shoppling_path)

    # 2) 온채널
    save_onchannel_xlsx(on_out, onchannel_path)

    # 3) 도매의신 (0건이면 파일 생성 안 함)
    if not dom_out.empty:
        save_domesin_xls_with_xlwings(dom_out, domesin_path)
    else:
        domesin_path = None

    return shoppling_path, onchannel_path, domesin_path


# -----------------------------
# GUI
# -----------------------------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PIDPIC → 송장등록 파일 생성")
        self.resize(760, 210)

        self.pidpic_path: Path | None = None

        layout = QVBoxLayout(self)

        row1 = QHBoxLayout()
        self.pid_edit = QLineEdit()
        self.pid_edit.setReadOnly(True)
        btn_pick = QPushButton("PIDPIC 파일 선택")
        btn_pick.clicked.connect(self.pick_file)

        row1.addWidget(QLabel("PIDPIC:"))
        row1.addWidget(self.pid_edit, 1)
        row1.addWidget(btn_pick)
        layout.addLayout(row1)

        info = QLabel(
            f"저장 위치: {DOWNLOADS}\n"
            f"① 샵플링 송장등록.xlsx\n"
            f"② 온채널 송장등록.xlsx\n"
            f"③ 도매의신 송장등록.xls (도매의신 주문 있을 때만)"
        )
        info.setStyleSheet("color:#555;")
        layout.addWidget(info)

        btn_run = QPushButton("다운로드 폴더에 3개 파일 생성")
        btn_run.setStyleSheet("font-size:16px; font-weight:700; padding:10px;")
        btn_run.clicked.connect(self.run)
        layout.addWidget(btn_run)

        self.status = QLabel("대기 중")
        layout.addWidget(self.status)

    def pick_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "PIDPIC 파일 선택", str(DOWNLOADS),
            "Excel Files (*.xlsx *.xls)"
        )
        if path:
            self.pidpic_path = Path(path)
            self.pid_edit.setText(str(self.pidpic_path))

    def run(self):
        if not self.pidpic_path or not self.pidpic_path.exists():
            QMessageBox.warning(self, "오류", "PIDPIC 파일을 먼저 선택하세요.")
            return

        try:
            self.status.setText("생성 중...")
            shoppling_path, onchannel_path, domesin_path = save_files_vba_compatible(self.pidpic_path)

            msg = (
                "✅ 다운로드 폴더에 파일 저장 완료!\n\n"
                f"① {shoppling_path}\n"
                f"② {onchannel_path}\n"
                f"③ {domesin_path if domesin_path else '도매의신 주문 없음(생성 안 함)'}"
            )
            QMessageBox.information(self, "완료", msg)
            self.status.setText("완료")
        except Exception as e:
            QMessageBox.critical(self, "실패", f"에러:\n{e}")
            self.status.setText("실패")


def main():
    app = QApplication.instance() or QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()


if __name__ == "__main__":
    main()