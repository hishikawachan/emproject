"""
Thincacloud 端末・売上管理システム - インカム検索 自動化スクリプト
対象URL: toamas-amusement.thincacloud.com
操作内容:
  1. ログイン（既存セッション利用 or 新規ログイン）
  2. 売上管理 → インカム検索 メニューへ遷移
  3. 検索期間（自・至）をカレンダーUIで入力
  4. 検索実行
  5. 結果一覧のCSVをダウンロード
"""

import time
import os
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# ============================================================
# 設定値（必要に応じて変更してください）
# ============================================================
CONFIG = {
    # サイトURL
    "base_url": "https://toamas-amusement.thincacloud.com",

    # ログイン情報（ログインが必要な場合に使用）
    "username": "YOUR_USERNAME",
    "password": "YOUR_PASSWORD",

    # 検索期間
    # Noneにすると「前週の月曜00:00 〜 今週の日曜23:59」が自動設定されます
    # 手動指定する場合は "YYYY-MM-DD HH:MM" 形式で記入
    "date_from": None,   # 例: "2026-04-06 03:00"
    "date_to":   None,   # 例: "2026-04-13 23:59"

    # CSVダウンロード先フォルダ（絶対パスを推奨）
    "download_dir": os.path.join(os.path.expanduser("~"), "Downloads"),

    # Chromeドライバーのパス（Noneの場合はPATHから自動検索）
    "chromedriver_path": None,

    # ブラウザを表示するか（False=ヘッドレスモード）
    "headless": False,

    # 各操作の待機秒数（ページ読み込みが遅い場合は増やす）
    "wait_timeout": 20,
}


def get_default_date_range():
    """前週月曜00:00 〜 今週日曜23:59 を返す"""
    today = datetime.now()
    # 今週の月曜日
    monday = today - timedelta(days=today.weekday())
    # 前週の月曜日
    last_monday = monday - timedelta(weeks=1)
    # 先週の日曜日（今週月曜の前日）
    last_sunday = monday - timedelta(days=1)

    date_from = last_monday.replace(hour=0, minute=0, second=0)
    date_to   = last_sunday.replace(hour=23, minute=59, second=0)
    return date_from, date_to


def build_driver(config: dict) -> webdriver.Chrome:
    """Chrome WebDriverを構築して返す"""
    options = Options()

    if config["headless"]:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

    # ダウンロードフォルダ設定
    download_dir = os.path.abspath(config["download_dir"])
    os.makedirs(download_dir, exist_ok=True)
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    options.add_experimental_option("prefs", prefs)

    # その他オプション
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    if config["chromedriver_path"]:
        service = Service(executable_path=config["chromedriver_path"])
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(5)
    return driver


def wait_and_click(driver, by, selector, timeout=20):
    """要素が clickable になるまで待ってクリック"""
    el = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, selector))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
    time.sleep(0.3)
    el.click()
    return el


def wait_visible(driver, by, selector, timeout=20):
    """要素が visible になるまで待って返す"""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, selector))
    )


def is_logged_in(driver, base_url: str) -> bool:
    """ログイン済みかどうかを確認する"""
    driver.get(base_url)
    time.sleep(2)
    # ログイン画面にいる場合はログインフォームが存在する
    try:
        driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        return False
    except NoSuchElementException:
        return True


def login(driver, config: dict):
    """ログイン処理"""
    base_url = config["base_url"]
    print("[ログイン] ログインページへアクセス...")
    driver.get(base_url)
    time.sleep(2)

    try:
        # ユーザー名入力
        username_input = wait_visible(driver, By.CSS_SELECTOR,
                                      "input[type='text'], input[name*='user'], input[name*='login'], input[name*='id']",
                                      timeout=10)
        username_input.clear()
        username_input.send_keys(config["username"])

        # パスワード入力
        password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        password_input.clear()
        password_input.send_keys(config["password"])

        # ログインボタン
        login_btn = driver.find_element(
            By.XPATH,
            "//button[contains(text(),'ログイン') or contains(text(),'Login') or contains(text(),'サインイン')]"
            " | //input[@type='submit']"
        )
        login_btn.click()
        time.sleep(3)
        print("[ログイン] ログイン完了")
    except Exception as e:
        print(f"[警告] ログイン処理でエラーが発生しました: {e}")
        print("  → すでにログイン済みの場合は続行します")


def navigate_to_income_search(driver, config: dict):
    """売上管理 → インカム検索 へ遷移"""
    base_url = config["base_url"]
    timeout  = config["wait_timeout"]

    print("[ナビ] 売上管理メニューをクリック...")
    # 「売上管理」メニューボタンをクリック
    wait_and_click(
        driver,
        By.XPATH,
        "//a[contains(text(),'売上管理')] | //*[contains(@class,'nav') and contains(text(),'売上管理')]",
        timeout=timeout,
    )
    time.sleep(0.8)

    print("[ナビ] インカム検索をクリック...")
    # ドロップダウンの「インカム検索」をクリック
    wait_and_click(
        driver,
        By.XPATH,
        "//a[contains(text(),'インカム検索')] | //li[contains(text(),'インカム検索')]",
        timeout=timeout,
    )
    time.sleep(1.5)

    # /MS01 ページが開いたことを確認
    WebDriverWait(driver, timeout).until(
        lambda d: "MS01" in d.current_url or "インカム検索" in d.title
    )
    print(f"[ナビ] インカム検索ページへ遷移完了: {driver.current_url}")


def set_datetime_field(driver, field_label_xpath: str, dt: datetime, timeout: int = 20):
    """
    カレンダーUIで日時を入力する。
    手順:
      1. 入力フィールドをクリック → カレンダーポップアップ表示
      2. 年月を合わせる（< > ボタンで移動）
      3. 日付をクリック
      4. 時刻（時・分）を直接入力
      5. カレンダー外をクリックして閉じる
    """
    label = "自" if "自" in field_label_xpath else "至"
    print(f"[日時入力] 「{label}」フィールドに {dt.strftime('%Y-%m-%d %H:%M')} を設定...")

    # ─── 入力フィールドをクリックしてカレンダーを開く ───
    field_input = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, field_label_xpath))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", field_input)
    time.sleep(0.3)
    field_input.click()
    time.sleep(0.8)

    # ─── カレンダーポップアップが表示されるまで待つ ───
    calendar = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".vc-container, .calendar, [class*='calendar'], [class*='datepicker']"))
    )

    # ─── 年月を合わせる ───
    target_year  = dt.year
    target_month = dt.month

    for _ in range(24):  # 最大24ヶ月移動
        # 現在表示中の年月を取得
        try:
            header_text = driver.find_element(
                By.CSS_SELECTOR,
                ".vc-title, [class*='calendar-title'], [class*='month-year'], [class*='header']"
            ).text
        except NoSuchElementException:
            break

        # "2026年 4月" のような文字列をパース
        import re
        m = re.search(r'(\d{4})', header_text)
        month_map = {"1月":1,"2月":2,"3月":3,"4月":4,"5月":5,"6月":6,
                     "7月":7,"8月":8,"9月":9,"10月":10,"11月":11,"12月":12,
                     "Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,
                     "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}

        cur_year  = int(m.group(1)) if m else target_year
        cur_month = target_month  # デフォルト

        for k, v in month_map.items():
            if k in header_text:
                cur_month = v
                break

        if cur_year == target_year and cur_month == target_month:
            break

        # 前月 or 翌月ボタンを押す
        if (cur_year, cur_month) > (target_year, target_month):
            # 前月へ
            prev_btn = driver.find_element(
                By.CSS_SELECTOR,
                ".vc-arrow.is-left, [class*='prev'], button[aria-label*='前'], button[aria-label*='prev']"
            )
            prev_btn.click()
        else:
            # 翌月へ
            next_btn = driver.find_element(
                By.CSS_SELECTOR,
                ".vc-arrow.is-right, [class*='next'], button[aria-label*='次'], button[aria-label*='next']"
            )
            next_btn.click()
        time.sleep(0.4)

    # ─── 日付をクリック ───
    day_str = str(dt.day)
    # カレンダーの日付セルをXPathで探す（グレーアウトしていない当月の日付）
    day_xpath = (
        f"//div[contains(@class,'vc-day') and not(contains(@class,'is-not-in-month'))]"
        f"//span[normalize-space(text())='{day_str}']"
        f" | "
        f"//td[not(contains(@class,'disabled'))]//*[normalize-space(text())='{day_str}']"
    )
    try:
        day_el = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, day_xpath))
        )
        day_el.click()
        time.sleep(0.5)
    except TimeoutException:
        # フォールバック: テキストが一致するすべてのセルから当月分を探す
        cells = driver.find_elements(By.XPATH, f"//*[normalize-space(text())='{day_str}']")
        for c in cells:
            try:
                c.click()
                break
            except Exception:
                continue
        time.sleep(0.5)

    # ─── 時刻を入力（時・分の spinbox or input） ───
    # カレンダー下部の時刻フィールド
    time_inputs = driver.find_elements(
        By.CSS_SELECTOR,
        ".vc-time-picker input, [class*='time'] input, [class*='hour'] input, [class*='minute'] input"
    )

    if len(time_inputs) >= 2:
        # 時（hour）
        hour_input = time_inputs[0]
        _set_time_input(driver, hour_input, dt.hour)
        time.sleep(0.3)
        # 分（minute）
        min_input = time_inputs[1]
        _set_time_input(driver, min_input, dt.minute)
        time.sleep(0.3)
    elif len(time_inputs) == 1:
        # 時と分が同じ input の場合
        _set_time_input(driver, time_inputs[0], dt.hour)
    else:
        # spinbox形式（上下矢印ボタンで調整）
        _adjust_time_spinbox(driver, dt)

    time.sleep(0.3)

    # ─── カレンダーを閉じる（カレンダー外をクリック） ───
    try:
        driver.find_element(By.CSS_SELECTOR, "h2, .page-title, main").click()
    except Exception:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
    time.sleep(0.5)
    print(f"[日時入力] 「{label}」設定完了")


def _set_time_input(driver, input_el, value: int):
    """時刻 input 要素に値をセットする"""
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", input_el)
    input_el.click()
    time.sleep(0.2)
    input_el.send_keys(Keys.CONTROL + "a")
    input_el.send_keys(str(value).zfill(2))
    input_el.send_keys(Keys.TAB)


def _adjust_time_spinbox(driver, dt: datetime):
    """
    spinbox形式（上下矢印ボタン）で時刻を調整するフォールバック。
    動画を見ると、時フィールドをクリック→値を直接タイプ、分フィールドも同様。
    """
    # 時フィールドを特定（数値のみが入るフィールド）
    spinboxes = driver.find_elements(
        By.CSS_SELECTOR,
        "input[type='number'], .vc-time-picker input"
    )
    if len(spinboxes) >= 1:
        h_input = spinboxes[0]
        h_input.triple_click() if hasattr(h_input, 'triple_click') else None
        h_input.click()
        h_input.send_keys(Keys.CONTROL + "a")
        h_input.send_keys(str(dt.hour).zfill(2))

    if len(spinboxes) >= 2:
        m_input = spinboxes[1]
        m_input.click()
        m_input.send_keys(Keys.CONTROL + "a")
        m_input.send_keys(str(dt.minute).zfill(2))


def set_search_period(driver, date_from: datetime, date_to: datetime, timeout: int = 20):
    """
    インカム検索画面の検索期間（自・至）を設定する。
    動画の観察結果:
      - 「自」フィールドをクリック → カレンダーが開く → 日付選択 → 時刻入力
      - 「至」フィールドをクリック → カレンダーが開く → 日付選択 → 時刻入力
    """
    # ─── 「自」フィールド ───
    # XPath: プレースホルダーに "自" か "省略時" という文字を含む入力フィールド
    from_xpath = (
        "//input[contains(@placeholder,'自') or contains(@placeholder,'省略') or contains(@placeholder,'From')]"
        "[1]"
        " | "
        "(//label[contains(text(),'自')]/following-sibling::input | //label[contains(text(),'自')]/..//input)[1]"
    )
    set_datetime_field(driver, from_xpath, date_from, timeout)
    time.sleep(0.5)

    # ─── 「至」フィールド ───
    to_xpath = (
        "//input[contains(@placeholder,'至') or contains(@placeholder,'To')]"
        "[1]"
        " | "
        "(//label[contains(text(),'至')]/following-sibling::input | //label[contains(text(),'至')]/..//input)[1]"
    )
    set_datetime_field(driver, to_xpath, date_to, timeout)
    time.sleep(0.5)


def click_search(driver, timeout: int = 20):
    """「検索」ボタンをクリックして結果を待つ"""
    print("[検索] 検索ボタンをクリック...")
    wait_and_click(
        driver,
        By.XPATH,
        "//button[contains(text(),'検索')] | //a[contains(text(),'検索')] | //*[@class and contains(@class,'search') and (contains(text(),'検索') or contains(.,'検索'))]",
        timeout=timeout,
    )

    # 結果が表示されるまで待つ（件数テキスト or テーブル行）
    print("[検索] 結果を待っています...")
    try:
        WebDriverWait(driver, 30).until(
            lambda d: (
                d.find_elements(By.XPATH, "//*[contains(text(),'件')]") or
                d.find_elements(By.CSS_SELECTOR, "table tbody tr")
            )
        )
    except TimeoutException:
        print("[警告] 結果の表示確認がタイムアウトしました。処理を継続します。")

    time.sleep(1)

    # 件数を表示
    try:
        count_el = driver.find_element(By.XPATH, "//*[contains(text(),'件') and string-length(text()) < 20]")
        print(f"[検索] 結果: {count_el.text.strip()}")
    except NoSuchElementException:
        print("[検索] 検索完了（件数テキストが見つかりませんでした）")


def download_csv(driver, config: dict):
    """
    検索結果のCSVをダウンロードする。
    動画では結果一覧の下部に「CSV」ボタンがある。
    また左下に「CSV出力」ボタン（検索前から常時表示）もある。
    """
    timeout = config["wait_timeout"]
    print("[CSV] CSVダウンロードボタンをクリック...")

    # 結果一覧下部の「CSV」ボタンを優先
    csv_xpath = (
        "//button[normalize-space(text())='CSV' or contains(text(),'CSV')]"
        " | "
        "//a[normalize-space(text())='CSV' or contains(text(),'CSV')]"
        " | "
        "//*[contains(@class,'csv') or contains(@class,'CSV')]"
    )

    # 複数ある場合は結果エリア内（右側メインコンテンツ）のボタンを優先
    try:
        csv_buttons = driver.find_elements(By.XPATH, csv_xpath)
        target_btn = None

        for btn in csv_buttons:
            # 「CSV出力」（左サイドバー）ではなく「CSV」（結果下部）を選ぶ
            btn_text = btn.text.strip()
            if btn_text in ("CSV", "▲CSV", "↓CSV", "CSVダウンロード"):
                target_btn = btn
                break

        if target_btn is None and csv_buttons:
            target_btn = csv_buttons[-1]  # 最後のボタン（通常は結果下部のもの）

        if target_btn:
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", target_btn)
            time.sleep(0.5)
            target_btn.click()
        else:
            raise NoSuchElementException("CSVボタンが見つかりません")

    except Exception as e:
        print(f"[警告] CSVボタンの特定に失敗: {e}")
        # フォールバック: テキストで探す
        wait_and_click(driver, By.XPATH, csv_xpath, timeout=timeout)

    # ダウンロード完了を待つ（.crdownload ファイルが消えるまで）
    print("[CSV] ダウンロード待機中...")
    download_dir = os.path.abspath(config["download_dir"])
    _wait_for_download(download_dir, timeout=30)
    print(f"[CSV] ダウンロード完了 → 保存先: {download_dir}")


def _wait_for_download(download_dir: str, timeout: int = 30):
    """ダウンロードが完了するまで待つ（.crdownload が消えるまで）"""
    deadline = time.time() + timeout
    while time.time() < deadline:
        crdownloads = [f for f in os.listdir(download_dir) if f.endswith(".crdownload")]
        if not crdownloads:
            time.sleep(1)  # 念のため少し待つ
            return
        time.sleep(0.5)
    print("[警告] ダウンロードタイムアウト。ファイルが不完全な可能性があります。")


def main():
    print("=" * 60)
    print("Thincacloud インカム検索 自動化スクリプト")
    print("=" * 60)

    # 日付範囲を決定
    if CONFIG["date_from"] and CONFIG["date_to"]:
        date_from = datetime.strptime(CONFIG["date_from"], "%Y-%m-%d %H:%M")
        date_to   = datetime.strptime(CONFIG["date_to"],   "%Y-%m-%d %H:%M")
    else:
        date_from, date_to = get_default_date_range()

    print(f"[設定] 検索期間: {date_from.strftime('%Y-%m-%d %H:%M')} ～ {date_to.strftime('%Y-%m-%d %H:%M')}")
    print(f"[設定] ダウンロード先: {CONFIG['download_dir']}")

    driver = build_driver(CONFIG)
    wait   = CONFIG["wait_timeout"]

    try:
        # ① ログイン確認 / ログイン
        if not is_logged_in(driver, CONFIG["base_url"]):
            login(driver, CONFIG)
        else:
            print("[ログイン] 既存セッションでログイン済みです")

        # ② インカム検索ページへ遷移
        navigate_to_income_search(driver, CONFIG)

        # ③ 検索期間を入力
        set_search_period(driver, date_from, date_to, timeout=wait)

        # ④ 検索実行
        click_search(driver, timeout=wait)

        # ⑤ CSVダウンロード
        download_csv(driver, CONFIG)

        print("\n✅ 全処理が完了しました！")

    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

        # エラー時にスクリーンショットを保存
        try:
            ss_path = os.path.join(CONFIG["download_dir"], "error_screenshot.png")
            driver.save_screenshot(ss_path)
            print(f"   スクリーンショットを保存しました: {ss_path}")
        except Exception:
            pass

    finally:
        time.sleep(2)
        driver.quit()
        print("[終了] ブラウザを閉じました")


if __name__ == "__main__":
    main()