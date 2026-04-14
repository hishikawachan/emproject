"""
Thincacloud 端末・売上管理システム 自動ログインスクリプト
対象URL: https://toamas-amusement.thincacloud.com/Logon

【使い方】
1. 依存ライブラリをインストール:
   pip install selenium webdriver-manager

2. 環境変数をセット（推奨）:
   export AFFILIATION_CODE=0158
   export ACCOUNT_ID=001144001001
   export LOGIN_PASSWORD=KW708kiwa

   または、スクリプト実行時に直接入力も可能（後述）

3. 実行:
   python thincacloud_login.py
"""

import os
import time
import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import platform

try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_WDM = True
except ImportError:
    USE_WDM = False

# ============================================================
# 設定：環境変数から読み込む（なければ対話入力）
# ============================================================
#AFFILIATION_CODE = os.environ.get("AFFILIATION_CODE") or input("所属コードを入力: ").strip()
#ACCOUNT_ID       = os.environ.get("ACCOUNT_ID")       or input("アカウントIDを入力: ").strip()
#LOGIN_PASSWORD   = os.environ.get("LOGIN_PASSWORD")   or getpass.getpass("パスワードを入力: ")

AFFILIATION_CODE = input("所属コードを入力: ").strip()
ACCOUNT_ID       = input("アカウントIDを入力: ").strip()
LOGIN_PASSWORD   = input("パスワードを入力: ").strip()


LOGIN_URL = "https://toamas-amusement.thincacloud.com/Logon"
WAIT_SEC  = 15  # 要素待機タイムアウト（秒）

OS_NAME = platform.system()

def build_driver(headless: bool = False) -> webdriver.Chrome:
    """ChromeDriverを生成して返す。"""
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,900")

    if USE_WDM:
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    else:
        # ChromeDriver が PATH に存在する場合
        return webdriver.Chrome(options=options)


def find_input(wait: WebDriverWait, *strategies):
    """
    複数の (By, selector) タプルを順に試し、最初に見つかった要素を返す。
    動的SPAでは要素名が変わることがあるため複数候補を保持する。
    """
    for by, selector in strategies:
        try:
            return wait.until(EC.element_to_be_clickable((by, selector)))
        except TimeoutException:
            continue
    raise NoSuchElementException(
        f"いずれのセレクタでも要素が見つかりませんでした: {strategies}"
    )


def login():
    driver = build_driver(headless=False)  # 動作確認後は headless=True に変更可
    wait   = WebDriverWait(driver, WAIT_SEC)

    try:
        print(f"[1/5] ページを開いています: {LOGIN_URL}")
        driver.get(LOGIN_URL)

        # ── 所属コード ──────────────────────────────────────────
        # SPAのため、実際のname/id/placeholderをブラウザのDevToolsで確認して
        # 下記候補リストに追加・修正してください。
        print("[2/5] 所属コードを入力しています...")
        """ field_affiliation = find_input(
            wait,
            (By.NAME,        "affiliationCode"),
            (By.NAME,        "affiliation_code"),
            (By.NAME,        "soshokuCode"),
            (By.ID,          "affiliationCode"),
            (By.ID,          "affiliation-code"),
            (By.CSS_SELECTOR, "input[placeholder*='所属']"),
            (By.CSS_SELECTOR, "input[placeholder*='Affiliation']"),
            (By.XPATH,        "//input[@type='text'][1]"),  # フォーム内1番目のテキスト入力
            (By.XPATH,        "//*[@id='input-39']"),
        ) """
        field_affiliation = find_input(
            wait,
            (By.XPATH,        "//*[@id='input-39']"),
        )
        field_affiliation.clear()
        field_affiliation.send_keys(AFFILIATION_CODE)

        # ── アカウントID ─────────────────────────────────────────
        print("[3/5] アカウントIDを入力しています...")  
        """ field_account = find_input(
            wait,
            (By.NAME,        "accountId"),
            (By.NAME,        "account_id"),
            (By.NAME,        "loginId"),
            (By.NAME,        "userId"),
            (By.ID,          "accountId"),
            (By.ID,          "account-id"),
            (By.CSS_SELECTOR, "input[placeholder*='アカウント']"),
            (By.CSS_SELECTOR, "input[placeholder*='Account']"),
            (By.XPATH,        "//input[@type='text'][2]"),  # フォーム内2番目のテキスト入力
            (By.XPATH,        "//*[@id='logon-id']"),       
        ) """
        field_account = find_input(
            wait,
            (By.XPATH,        "//*[@id='logon-id']"),       
        )
        field_account.clear()
        field_account.send_keys(ACCOUNT_ID)

        # ── パスワード ───────────────────────────────────────────
        print("[4/5] パスワードを入力しています...")
        """ field_password = find_input(
            wait,
            (By.NAME,        "password"),
            (By.NAME,        "passwd"),
            (By.NAME,        "pass"),
            (By.ID,          "password"),
            (By.CSS_SELECTOR, "input[type='password']"),
            (By.XPATH,        "//*[@id='password']"), 
        ) """
        field_password = find_input(
            wait,
            (By.XPATH,        "//*[@id='password']"), 
        )
        field_password.clear()
        field_password.send_keys(LOGIN_PASSWORD)

        # ── ログインボタン ────────────────────────────────────────
        print("[5/5] ログインボタンをクリックしています...")
        """  btn_login = find_input(
            wait,
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.CSS_SELECTOR, "input[type='submit']"),
            (By.XPATH,        "//button[contains(text(),'ログイン')]"),
            (By.XPATH,        "//button[contains(text(),'Login')]"),
            (By.XPATH,        "//button[contains(text(),'ログオン')]"),
            (By.XPATH,        "//input[@value='ログイン']"),
            (By.XPATH,        "//*[@id='app']/div[2]/div/form/div/div[3]/button/span"),
        ) """
        btn_login = find_input(
            wait,
            (By.XPATH,        "//*[@id='app']/div[2]/div/form/div/div[3]/button/span"),
        )
        btn_login.click()

        # ── ログイン結果の確認 ─────────────────────────────────
        time.sleep(3)
        current_url = driver.current_url
        page_title  = driver.title

        if "Logon" not in current_url and "login" not in current_url.lower():
            print(f"\n✅ ログイン成功！")
            print(f"   遷移先URL : {current_url}")
            print(f"   ページタイトル: {page_title}")
        else:
            print(f"\n⚠️  ログインページに留まっています。認証情報またはセレクタを確認してください。")
            print(f"   現在のURL: {current_url}")

        # ブラウザをそのまま開けておく（確認用）
        input("\n[Enter]キーでブラウザを閉じます...")

    except NoSuchElementException as e:
        print(f"\n❌ 要素が見つかりませんでした: {e}")
        print("   ページのHTMLをDevToolsで確認し、セレクタを修正してください。")
        input("[Enter]で終了...")

    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        input("[Enter]で終了...")

    finally:
        driver.quit()


if __name__ == "__main__":
    login()