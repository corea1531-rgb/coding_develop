# collectors.py (온채널 파트)

import os, time, glob
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json


DOWNLOAD_DIR = str(Path.home() / "Downloads")


def load_accounts_json() -> dict:
    base_dir = Path(__file__).resolve().parent  # collectors.py 폴더
    path = base_dir / "accounts.json"
    if not path.exists():
        default = {
            "onchannel": {
                "sm": {"id": "", "pw": ""},
                "km": {"id": "", "pw": ""}
            },
            "domesin": {"id": "", "pw": ""}
        }
        path.write_text(json.dumps(default, ensure_ascii=False, indent=2), encoding="utf-8")
        return default

    return json.loads(path.read_text(encoding="utf-8"))

def collect_all_by_accounts(logger=None, accounts: Optional[dict] = None):
    """
    accounts.json 기반으로 온채널(SM/KM) + 도매의신 수집 실행
    반환: (onch_path, df_domesin)
    """
    if accounts is None:
        accounts = load_accounts_json()

    def log(msg: str):
        if logger:
            logger(msg)

    onch = accounts.get("onchannel", {})
    sm_id = onch.get("sm", {}).get("id", "")
    sm_pw = onch.get("sm", {}).get("pw", "")
    km_id = onch.get("km", {}).get("id", "")
    km_pw = onch.get("km", {}).get("pw", "")

    dm = accounts.get("domesin", {})
    dm_id = dm.get("id", "")
    dm_pw = dm.get("pw", "")

    # ---- 필수값 체크
    if not all([sm_id, sm_pw, km_id, km_pw]):
        raise ValueError("온채널 계정 정보가 비어있습니다. accounts.json의 onchannel.sm/km id/pw를 확인하세요.")
    if not all([dm_id, dm_pw]):
        raise ValueError("도매의신 계정 정보가 비어있습니다. accounts.json의 domesin id/pw를 확인하세요.")

    log("✅ 성민에셋 온채널 주문수집중")
    onch_path = collect_onchannel_all(
        sm_id=sm_id, sm_pw=sm_pw,
        km_id=km_id, km_pw=km_pw,
        logger=log
    )

    log("✅ 도매의신 주문수집중")
    df_dm, _ = collect_domesin_orders(
        user_ID=dm_id,
        user_PW=dm_pw,
        logger=log,
        save_excel=True
    )

    return onch_path, df_dm

def make_driver(download_dir: str, headless: bool = True):
    options = Options()

    # ✅ headless 옵션을 켜고/끄고 선택 가능
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

    # ✅ 안정성 옵션
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-notifications")
    options.add_argument("--lang=ko-KR")

    # ✅ 다운로드 경로 고정(온채널 다운로드용)
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)

    # ✅ headless에서 다운로드 막히는 환경 대비 (온채널용)
    try:
        driver.execute_cdp_cmd(
            "Page.setDownloadBehavior",
            {"behavior": "allow", "downloadPath": download_dir}
        )
    except Exception:
        pass

    return driver


def wait_download_complete(download_dir, pattern="supplier_order_list_*.xlsx", since_ts=None, need_count=1, timeout=120):
    end = time.time() + timeout
    while time.time() < end:
        crs = glob.glob(os.path.join(download_dir, "*.crdownload"))
        if since_ts is not None:
            crs = [c for c in crs if os.path.getmtime(c) >= since_ts]
        if crs:
            time.sleep(0.3)
            continue

        files = glob.glob(os.path.join(download_dir, pattern))
        if since_ts is not None:
            files = [f for f in files if os.path.getmtime(f) >= since_ts]
        files.sort(key=os.path.getmtime, reverse=True)

        if len(files) >= need_count:
            return files[:need_count]

        time.sleep(0.3)

    raise TimeoutError(f"다운로드된 {pattern} 파일을 시간 내에 찾지 못했어요.")


def merge_supplier_excels(file1, file2, out_path):
    df1 = pd.read_excel(file1, dtype=str)
    df2 = pd.read_excel(file2, dtype=str)

    cols = list(df1.columns)
    df2 = df2.reindex(columns=cols)

    merged = pd.concat([df1, df2], ignore_index=True)
    merged.to_excel(out_path, index=False)
    return out_path


def download_onchannel_excel(account_id, account_pw, account_name="ACCOUNT", logger=None):
    def log(msg: str):
        if logger:
            logger(msg)

    driver = make_driver(DOWNLOAD_DIR)
    wait = WebDriverWait(driver, 15)

    try:
        log(f"[{account_name}] 로그인 페이지 진입")
        driver.get('https://www.onch3.co.kr/login/login_web.php')

        ID = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.container > form > div:nth-child(2) > input')))
        ID.clear()
        ID.send_keys(account_id)

        PW = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.container > form > div:nth-child(3) > input')))
        PW.clear()
        PW.send_keys(account_pw)

        login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.container > form > button')))
        login_btn.click()

        log(f"[{account_name}] 대시보드 이동")
        driver.get('https://www.onch3.co.kr/mypage/dashboard.php?target=seller')

        seller_cate = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#kt_sidebar_menu > div:nth-child(8) > a > span.menu-title.text-gray-600')))
        seller_cate.click()

        oredr_info = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#kt_sidebar_menu > div.menu-item.menu-accordion.hover.show > div > div:nth-child(5) > a > span')))
        oredr_info.click()

        order_down_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#kt_app_wrapper > div.contentWrap > div.container.p-3 > div.contentWrap > div.card > div.card-header.min-h-auto.p-6.border-bottom-0.d-flex.justify-content-between.align-items-center > div > button.btn.btn-excel.me-2')))
        order_down_btn.click()

        today = datetime.today()
        start_day = today - timedelta(days=7)
        start_str = start_day.strftime("%Y-%m-%d")
        end_str   = today.strftime("%Y-%m-%d")
        start_sel = "#downExcelOrderListModal > div > div > div.modal-body.p-4 > div.row.align-items-center.mb-4 > div.col > div > input:nth-child(1)"
        end_sel   = "#downExcelOrderListModal > div > div > div.modal-body.p-4 > div.row.align-items-center.mb-4 > div.col > div > input:nth-child(3)"

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#downExcelOrderListModal")))

        def send_date(selector: str, value: str):
            el = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            driver.execute_script("""
                arguments[0].removeAttribute('readonly');
                arguments[0].removeAttribute('disabled');
            """, el)
            driver.execute_script("arguments[0].focus(); arguments[0].click();", el)
            el.send_keys(Keys.CONTROL, 'a')
            el.send_keys(Keys.DELETE)
            el.send_keys(value)
            el.send_keys(Keys.TAB)

        send_date(start_sel, start_str)
        send_date(end_sel, end_str)
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

        # alert
        try:
            alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
            log(f"[{account_name}] alert: {alert.text}")
            alert.accept()
        except Exception:
            pass

        agree = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#agreement-order-down-check")))
        if not agree.is_selected():
            driver.execute_script("arguments[0].click();", agree)

        t0 = time.time()

        down_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#btn-order-excel-down")))
        driver.execute_script("arguments[0].click();", down_btn)

        try:
            alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
            log(f"[{account_name}] alert: {alert.text}")
            alert.accept()
        except Exception:
            pass

        downloaded_file = wait_download_complete(DOWNLOAD_DIR, since_ts=t0, need_count=1, timeout=120)[0]
        log(f"[{account_name}] 다운로드 완료")

        return downloaded_file

    finally:
        try:
            driver.quit()
        except Exception:
            pass


def collect_onchannel_all(sm_id, sm_pw, km_id, km_pw, logger=None) -> str:
    """
    SM 다운로드 → KM 다운로드 → 병합 저장 → out_path 반환
    """
    def log(msg: str):
        if logger:
            logger(msg)

    log("성민에셋 온채널 주문수집중")
    sm_file = download_onchannel_excel(sm_id, sm_pw, account_name="성민에셋", logger=logger)

    log("케이엠 온채널 주문수집중")
    km_file = download_onchannel_excel(km_id, km_pw, account_name="케이엠", logger=logger)

    out_path = os.path.join(DOWNLOAD_DIR, "온채널 주문내역.xlsx")
    try:
        merged_path = merge_supplier_excels(sm_file, km_file, out_path)
    except PermissionError:
        out_path = os.path.join(DOWNLOAD_DIR, f"온채널 주문내역_{time.strftime('%Y%m%d_%H%M%S')}.xlsx")
        merged_path = merge_supplier_excels(sm_file, km_file, out_path)

    log("***온채널 병합 파일 저장 완료***")
    return merged_path


# collectors.py (도매의신 파트)

import time
import re
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


def collect_domesin_orders(user_ID: str, user_PW: str, logger=None, save_excel: bool = True):
    """
    도매의신 주문 수집
    - return: (df, out_path or None)
    """
    def log(msg: str):
        if logger:
            logger(msg)

    driver = make_driver(DOWNLOAD_DIR, headless=True)   # ← 처음엔 False 권장(창 보이게)
    wait = WebDriverWait(driver, 15)

    # ----------------------------
    # 1) 주문 그룹핑
    # ----------------------------
    def is_header_tr(tr) -> bool:
        if tr.find("th"):
            return True
        txt = tr.get_text(" ", strip=True)
        return ("주문번호" in txt and "수취인명" in txt) or ("상품명" in txt and "공급가" in txt)

    def is_customerinfo_tr(tr) -> bool:
        txt = tr.get_text(" ", strip=True)
        return ("연락처1" in txt) and ("주소" in txt)

    def is_main_tr(tr) -> bool:
        txt = tr.get_text(" ", strip=True)
        has_date = re.search(r"\d{4}-\d{2}-\d{2}", txt) is not None
        has_order_no = re.search(r"\b20\d{10,}\b", txt) is not None
        return has_date or has_order_no

    def parse_orders_grouping(html: str, table_css="table.mytable2"):
        soup = BeautifulSoup(html, "html.parser")
        table = soup.select_one(table_css)
        if not table:
            raise ValueError("table.mytable2 를 못 찾음")

        trs = table.select("tbody > tr")

        orders = []
        current_items = []

        for tr in trs:
            if is_header_tr(tr):
                continue

            if is_customerinfo_tr(tr):
                cust_txt = tr.get_text(" ", strip=True)
                if current_items:
                    orders.append({
                        "items": current_items,
                        "customer_info_text": cust_txt
                    })
                    current_items = []
                continue

            if is_main_tr(tr):
                current_items.append(tr)
                continue

        return orders

    # ----------------------------
    # 2) 필드 추출
    # ----------------------------
    def extract_order_no(tr):
        d = tr.select_one("div[onclick*='view_order']")
        if not d:
            return ""
        txt = d.get_text(strip=True)
        if re.fullmatch(r"\d{10,}", txt):
            return txt
        oc = d.get("onclick", "")
        m = re.search(r"view_order\('(\d+)'\)", oc)
        return m.group(1) if m else txt

    def extract_receiver_from_first_tr(first_tr):
        td = first_tr.select_one("td[style*='font-weight:bold']")
        if td:
            return td.get_text(" ", strip=True)
        return ""

    def extract_supply_price(first_tr):
        tds = [td.get_text(" ", strip=True) for td in first_tr.find_all("td", recursive=False)]
        if not tds:
            return ""
        idx_prod = max(range(len(tds)), key=lambda i: len(tds[i]))
        for s in tds[idx_prod + 1:]:
            x = s.replace(",", "").replace(" ", "")
            if x.isdigit():
                return x
        return ""

    def extract_product_blob(first_tr):
        tds = [td.get_text(" ", strip=True) for td in first_tr.find_all("td", recursive=False)]
        return max(tds, key=len) if tds else ""

    def extract_product_pack(product_text: str):
        if not product_text:
            return "", "", "", "", ""

        flat = product_text.replace("\xa0", " ")
        flat = re.sub(r"\s+", " ", flat).strip()

        m_ts = re.search(r"\bTS\d+\b", flat)
        ts_code = m_ts.group(0) if m_ts else ""

        m_vendor = re.search(
            r"업체상품코드\s*[:：]?\s*([A-Z]{2}[_-]?[A-Z0-9]+(?:/[A-Z]{2}[_-]?[A-Z0-9]+)*)",
            flat
        )
        vendor_code = m_vendor.group(1) if m_vendor else ""

        m_inv = re.search(r"\(\s*택배송장명\s*[:：]\s*([^)]+?)\s*\)", flat)
        invoice_name = m_inv.group(1).strip() if m_inv else ""

        product_name = ""
        option_name = ""

        if vendor_code and m_inv:
            start = flat.find(vendor_code)
            if start != -1:
                start += len(vendor_code)
                inv_pos = flat.find(m_inv.group(0), start)
                if inv_pos != -1:
                    product_name = flat[start:inv_pos].strip(" -/|")
                    after_paren = inv_pos + len(m_inv.group(0))
                    end_key = "택배업체선택"
                    end_pos = flat.find(end_key, after_paren)
                    if end_pos == -1:
                        option_name = flat[after_paren:].strip(" -/|")
                    else:
                        option_name = flat[after_paren:end_pos].strip(" -/|")

        if not product_name and vendor_code:
            start = flat.find(vendor_code)
            if start != -1:
                start += len(vendor_code)
                end_pos = flat.find("택배업체선택", start)
                chunk = flat[start:end_pos].strip() if end_pos != -1 else flat[start:].strip()
                chunk = re.sub(r"\(\s*택배송장명\s*[:：]\s*[^)]+\)", "", chunk).strip()
                if chunk:
                    product_name = chunk

        return ts_code, vendor_code, product_name, invoice_name, option_name

    def extract_customer_fields(customer_info_text: str):
        phone1 = ""
        phone2 = ""
        zipcode = ""
        address = ""
        request_msg = ""

        if not customer_info_text:
            return phone1, phone2, zipcode, address, request_msg

        txt = customer_info_text

        m1 = re.search(r"연락처1\s*:\s*([0-9\-]{9,13})", txt)
        m2 = re.search(r"연락처2\s*:\s*([0-9\-]{9,13})", txt)
        if m1:
            phone1 = m1.group(1)
        if m2:
            phone2 = m2.group(1)

        madd = re.search(r"주소\s*[:：]?\s*(.*?)(?=배송요청사항\s*[:：]|$)", txt)
        addr_raw = madd.group(1).strip() if madd else ""

        mzip = re.search(r"\(\s*우\s*[:：]\s*(\d{5})\s*\)", addr_raw)
        if mzip:
            zipcode = mzip.group(1)
        else:
            mzip2 = re.search(r"\(\s*(\d{5})\s*\)", addr_raw)
            if mzip2:
                zipcode = mzip2.group(1)
            else:
                mzip3 = re.search(r"\b우\s*[:：]\s*(\d{5})\b", addr_raw)
                if mzip3:
                    zipcode = mzip3.group(1)

        address = addr_raw
        address = re.sub(r"^\(\s*우\s*[:：]\s*\d{5}\s*\)\s*", "", address)
        address = re.sub(r"^\(\s*\d{5}\s*\)\s*", "", address)
        address = re.sub(r"\s*\|\s*$", "", address).strip()

        mreq = re.search(r"배송요청사항\s*[:：]\s*(.*)$", txt)
        if mreq:
            request_msg = mreq.group(1).strip()

        return phone1, phone2, zipcode, address, request_msg

    def extract_quantity(item_tr):
        b = item_tr.select_one("b[style*='color:blue']")
        if b:
            t = b.get_text(strip=True)
            return t if t.isdigit() else ""
        return ""

    def is_item_tr(tr) -> bool:
        return tr.select_one("b[style*='color:blue']") is not None

    def extract_order_datetime(first_tr):
        date_pat = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
        time_pat = re.compile(r"\b\d{2}:\d{2}:\d{2}\b")

        for td in first_tr.find_all("td", recursive=False):
            txt = td.get_text(" ", strip=True)

            m_date = date_pat.search(txt)
            if not m_date:
                continue

            m_time = time_pat.search(txt)
            if m_time:
                return f"{m_date.group(0)} {m_time.group(0)}"

            m_time2 = time_pat.search(first_tr.get_text(" ", strip=True))
            if m_time2:
                return f"{m_date.group(0)} {m_time2.group(0)}"

            return m_date.group(0)

        return ""

    def extract_order_status(base_tr):
        tds = base_tr.find_all("td", recursive=False)
        for td in tds:
            txt = td.get_text(" ", strip=True)
            if "발송완료" in txt or "배송준비중" in txt or "배송마감" in txt or "취소" in txt or "교환" in txt or "반품" in txt:
                return txt
        return ""

    def is_not_shipped(base_tr):
        status = extract_order_status(base_tr)
        return "발송완료" not in status

    def is_file_locked(path: Path) -> bool:
        if not path.exists():
            return False
        try:
            with open(path, "a", encoding="utf-8"):
                pass
            return False
        except PermissionError:
            return True
        except OSError:
            return True

    def make_save_path(base_dir: Path, base_name: str, ext: str = ".xlsx") -> Path:
        base_dir.mkdir(parents=True, exist_ok=True)
        base_path = base_dir / f"{base_name}{ext}"
        if is_file_locked(base_path):
            ts = time.strftime("%Y%m%d_%H%M%S")
            return base_dir / f"{base_name}_{ts}{ext}"
        return base_path

    try:
        log("도매의신 로그인 진입")
        driver.get("https://domesin.com/scm/login.html")

        ID = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.login-box > form > input[type=text]:nth-child(4)")))
        ID.clear()
        ID.send_keys(user_ID)

        PW = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div > form > input[type=password]:nth-child(5)")))
        PW.clear()
        PW.send_keys(user_PW)

        login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div > form > button.login-btn")))
        login_btn.click()

        log("주문관리 페이지 이동")
        order_page = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > table > tbody > tr > td:nth-child(1) > ul:nth-child(5) > li:nth-child(1) > a")))
        driver.execute_script("arguments[0].click();", order_page)

        log("신규주문 선택/확인 처리")
        new_order = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#main > table.mytable1 > tbody > tr:nth-child(2) > td.cttd > input[type=radio]:nth-child(2)")))
        driver.execute_script('arguments[0].click()', new_order)

        select_tag = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#main > table.mytable1 > tbody > tr:nth-child(5) > td.cttd > select:nth-child(2)")))
        Select(select_tag).select_by_visible_text("100개씩 출력")

        select_order = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#main > table.mytable2 > tbody > tr:nth-child(1) > td:nth-child(1) > input[type=checkbox]')))
        driver.execute_script('arguments[0].click()', select_order)

        select_order = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#main > div > input:nth-child(1)')))
        driver.execute_script('arguments[0].click()', select_order)

        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        log(f"alert: {alert.text}")
        alert.accept()

        time.sleep(1.0)

        log("전체주문 선택/검색")
        total_order = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#main > table.mytable1 > tbody > tr:nth-child(2) > td.cttd > input[type=radio]:nth-child(1)")))
        total_order.click()

        select_tag = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#main > table.mytable1 > tbody > tr:nth-child(5) > td.cttd > select:nth-child(2)")))
        Select(select_tag).select_by_visible_text("100개씩 출력")

        order_search = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#main > table.mytable1 > tbody > tr:nth-child(5) > td.cttd > input.mybt02")))
        driver.execute_script("arguments[0].click();", order_search)
        time.sleep(1)

        html = driver.page_source
        orders = parse_orders_grouping(html)

        rows = []
        for od in orders:
            if not od.get("items"):
                continue

            item_trs = [tr for tr in od["items"] if is_item_tr(tr)]
            if not item_trs:
                continue

            base_tr = item_trs[0]
            if not is_not_shipped(base_tr):
                continue

            order_no = extract_order_no(base_tr)
            receiver = extract_receiver_from_first_tr(base_tr)
            order_dt = extract_order_datetime(base_tr)

            phone1, phone2, zipcode, address, request_msg = extract_customer_fields(
                od.get("customer_info_text", "")
            )

            for item_tr in item_trs:
                product_blob = extract_product_blob(item_tr)
                ts_code, vendor_code, product_name, invoice_name, option_name = extract_product_pack(product_blob)

                supply = extract_supply_price(item_tr)
                quantity = extract_quantity(item_tr)

                rows.append({
                    "주문코드": order_no,
                    "택배사코드": "",
                    "송장번호": "",
                    "수취인": receiver,
                    "수취인휴대폰": phone1,
                    "수취인전화": phone2,
                    "우편번호": zipcode,
                    "주소": address,
                    "상품코드": ts_code,
                    "업체상품코드": vendor_code,
                    "상품명": product_name,
                    "택배상품명": invoice_name,
                    "제조사": "케이엠트레이드",
                    "선택옵션": option_name,
                    "옵션관리코드": "",
                    "입력옵션": "",
                    "과세여부": "과세",
                    "공급가": supply,
                    "수량": quantity,
                    "배송구분":"기본배송",
                    "배송비":"3000",
                    "주문일시": order_dt,
                    "주문상태":"",
                    "배송처리일":"",
                    "주문요청사항":request_msg,
                    "주문원장고유번호":"",
                    "주문취소상태":"",
                    "주문반품상태":"",
                    "주문교환상태":"",
                })

        df = pd.DataFrame(rows)
        log(f"도매의신 수집 행수: {len(df)}")

        out_path = None
        if save_excel:
            save_dir = Path.home() / "Downloads"
            out_path = make_save_path(save_dir, "도매의신 주문내역", ".xlsx")
            df.to_excel(out_path, index=False)
            log("***도매의신 저장 완료***")

        return df, out_path

    finally:
        try:
            driver.quit()
        except Exception:
            pass