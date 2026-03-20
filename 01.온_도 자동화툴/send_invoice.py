# send_invoice.py
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Callable, Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from collectors import make_driver, DOWNLOAD_DIR


def _log(logger: Optional[Callable[[str], None]], msg: str):
    if logger:
        logger(msg)
    else:
        print(msg)


# ======================================================
# accounts.json 로드 (배포 안정형)
# 1) exe 옆 accounts.json 우선
# 2) 없으면 _internal/accounts.json
# 3) 개발 실행 시: send_invoice.py와 같은 폴더 accounts.json
# ======================================================
def _get_accounts_path() -> Path:
    if getattr(sys, "frozen", False):
        base = Path(sys.executable).resolve().parent  # dist/AutoTool
        p1 = base / "accounts.json"
        if p1.exists():
            return p1
        return base / "_internal" / "accounts.json"
    return Path(__file__).resolve().parent / "accounts.json"


def load_accounts_json() -> dict:
    path = _get_accounts_path()
    if not path.exists():
        raise FileNotFoundError(f"accounts.json을 찾을 수 없습니다: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def get_onchannel_accounts(accounts: dict):
    onch = accounts.get("onchannel", {})
    sm = onch.get("sm", {})
    km = onch.get("km", {})

    sm_id = (sm.get("id") or "").strip()
    sm_pw = (sm.get("pw") or "").strip()
    km_id = (km.get("id") or "").strip()
    km_pw = (km.get("pw") or "").strip()

    if not all([sm_id, sm_pw, km_id, km_pw]):
        raise ValueError("온채널 계정 정보가 비어있습니다. accounts.json의 onchannel.sm/km id/pw를 확인하세요.")
    return sm_id, sm_pw, km_id, km_pw


def get_domesin_accounts(accounts: dict):
    dm = accounts.get("domesin", {})
    dm_id = (dm.get("id") or "").strip()
    dm_pw = (dm.get("pw") or "").strip()

    if not all([dm_id, dm_pw]):
        raise ValueError("도매의신 계정 정보가 비어있습니다. accounts.json의 domesin id/pw를 확인하세요.")
    return dm_id, dm_pw


# =========================
# 온채널 송장 업로드(한 계정)
# =========================
def _upload_onchannel_one(
    account_id: str,
    account_pw: str,
    account_name: str,
    logger: Optional[Callable[[str], None]] = None
):
    _log(logger, f"[온채널] {account_name} 로그인/업로드 시작")

    driver = make_driver(DOWNLOAD_DIR, headless=True)
    wait = WebDriverWait(driver, 15)

    try:
        driver.get("https://www.onch3.co.kr/login/login_web.php")

        # ID
        ID = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.container > form > div:nth-child(2) > input"))
        )
        ID.clear()
        ID.send_keys(account_id)

        # PW
        PW = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.container > form > div:nth-child(3) > input"))
        )
        PW.clear()
        PW.send_keys(account_pw)

        # 로그인
        login_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.container > form > button"))
        )
        login_btn.click()

        # 대시보드
        driver.get("https://www.onch3.co.kr/mypage/dashboard.php?target=seller")

        # 공급사 정보
        seller_cate = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#kt_sidebar_menu > div:nth-child(8) > a > span.menu-title.text-gray-600"))
        )
        seller_cate.click()

        # 주문 정보
        order_info = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#kt_sidebar_menu > div.menu-item.menu-accordion.hover.show > div > div:nth-child(5) > a > span"))
        )
        order_info.click()

        # 엑셀송장등록
        xl_pass = wait.until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                "#kt_app_wrapper > div.contentWrap > div.container.p-3 > div.contentWrap > div.card > "
                "div.card-header.min-h-auto.p-6.border-bottom-0.d-flex.justify-content-between.align-items-center > "
                "div > button.btn.btn-dark.me-2"
            ))
        )
        xl_pass.click()

        # 파일 첨부
        file_input = wait.until(EC.presence_of_element_located((By.ID, "excelFileUpload")))
        file_path = str(Path.home() / "Downloads" / "온채널 송장등록.xlsx")
        file_input.send_keys(file_path)

        # 동의
        agree_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#agreement-order-excel-check")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", agree_btn)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#agreement-order-excel-check")))
        driver.execute_script("arguments[0].click();", agree_btn)

        # 등록하기
        submit_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#btn-order-excel-regist")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_btn)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#btn-order-excel-regist")))
        driver.execute_script("arguments[0].click();", submit_btn)

        # 같은 창/새 탭 대응
        wait.until(lambda d: (len(d.window_handles) > 1) or ("admin_view_excel_list2.php" in d.current_url))
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])

        wait.until(EC.url_contains("admin_view_excel_list2.php"))

        # 송장번호 등록하기
        invoice_regist = wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(normalize-space(.), '송장번호 등록하기')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", invoice_regist)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(normalize-space(.), '송장번호 등록하기')]")))
        driver.execute_script("arguments[0].click();", invoice_regist)

        # ✅ 핵심: KM에서 alert가 안 뜨는 경우가 있어도 죽지 않게 처리
        try:
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            _log(logger, f"[온채널] {account_name} 결과: {alert.text}")
            alert.accept()
            _log(logger, f"[온채널] {account_name} ✅ 송장번호 등록이 완료되었습니다")
        except TimeoutException:
            _log(logger, f"[온채널] {account_name} 알림(alert) 없음 → 다음 단계로 진행")

    finally:
        try:
            driver.quit()
        except Exception:
            pass


# =========================
# 도매의신 송장 업로드
# =========================
def _upload_domesin(dm_id: str, dm_pw: str, logger: Optional[Callable[[str], None]] = None):
    _log(logger, "[도매의신] 로그인/업로드 시작")

    driver = make_driver(DOWNLOAD_DIR, headless=True)
    wait = WebDriverWait(driver, 15)

    try:
        driver.get("https://domesin.com/scm/login.html")

        ID = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.login-box > form > input[type=text]:nth-child(4)"))
        )
        ID.clear()
        ID.send_keys(dm_id)

        PW = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body > div > form > input[type=password]:nth-child(5)"))
        )
        PW.clear()
        PW.send_keys(dm_pw)

        login_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div > form > button.login-btn"))
        )
        login_btn.click()

        # 송장엑셀등록
        invoice_info = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "body > table > tbody > tr > td:nth-child(1) > ul:nth-child(5) > li:nth-child(7) > a"))
        )
        driver.execute_script("arguments[0].click();", invoice_info)

        # 파일 업로드
        file_input = wait.until(EC.presence_of_element_located((By.NAME, "upfile")))
        file_path = str(Path.home() / "Downloads" / "도매의신 송장등록.xls")
        file_input.send_keys(file_path)

        upload = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#main > form > table > tbody > tr:nth-child(2) > td.cttd > div:nth-child(2) > input"))
        )
        driver.execute_script("arguments[0].click();", upload)

        _log(logger, "[도매의신] 송장번호 등록이 완료되었습니다")

    finally:
        try:
            driver.quit()
        except Exception:
            pass


# =========================
# 외부에서 호출할 “단일 진입점”
# =========================
def run_send_invoice(logger: Optional[Callable[[str], None]] = None):
    downloads = Path.home() / "Downloads"

    on_file = downloads / "온채널 송장등록.xlsx"
    if not on_file.exists():
        raise FileNotFoundError("온채널 송장등록.xlsx 없음 (등록파일 생성부터 필요)")

    dm_file = downloads / "도매의신 송장등록.xls"

    accounts = load_accounts_json()
    sm_id, sm_pw, km_id, km_pw = get_onchannel_accounts(accounts)

    _log(logger, "=== 송장 전송: 온채널(SM) ===")
    _upload_onchannel_one(sm_id, sm_pw, "SM", logger=logger)

    _log(logger, "=== 송장 전송: 온채널(KM) ===")
    _upload_onchannel_one(km_id, km_pw, "KM", logger=logger)

    if dm_file.exists():
        dm_id, dm_pw = get_domesin_accounts(accounts)
        _log(logger, "=== 송장 전송: 도매의신 ===")
        _upload_domesin(dm_id, dm_pw, logger=logger)
    else:
        _log(logger, "ℹ️ 도매의신 송장등록.xls 없음 → 도매의신 전송 스킵(주문 없으면 정상)")


if __name__ == "__main__":
    run_send_invoice()