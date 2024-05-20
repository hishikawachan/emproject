from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Chrome Webドライバー の インスタンスを生成
driver = webdriver.Chrome()

# Webドライバーでログインページを起動
driver.get('https://toamas-amusement.thincacloud.com/Logon')

time.sleep(1)
#driver.maximize_window()

#ログイン情報入力
driver.find_element(By.ID,"input-39").send_keys("0158")
driver.find_element(By.ID,"logon-id").send_keys("001144001001")
driver.find_element(By.ID,"password").send_keys("KW708kiwa")

element = driver.find_element(By.XPATH,'//*[@id="app"]/div[2]/div/form/div/div[3]/button')
element.click()
time.sleep(3)

#各種メニュー画面に遷移
driver.get('https://toamas-amusement.thincacloud.com/')

time.sleep(2)

#インカム情報メニューを開く
element = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/header/div/div[3]/span[1]/button[1]/span/i')
element.click()
time.sleep(1)

element = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/nav[2]/div[1]/div[1]/div[1]/div/a')
element.click()
time.sleep(2)

element = driver.find_element(By.XPATH,'//*[@id="app"]/div/header/div/button/span/i')
element.click()
time.sleep(3)

#検索日時情報を入力し、検索開始
driver.find_element(By.ID,"input-110").send_keys("2024-05-11 03:00")
time.sleep(2)
driver.find_element(By.ID,"input-118").send_keys("2024-05-20 23:00")
time.sleep(2)

element = driver.find_element(By.XPATH,'//*[@id="searchButtonArea"]/div/div/div[2]/button')
element.click()
time.sleep(5)

#検索したデータをフォルダに保存
element = driver.find_element(By.XPATH,'//*[@id="app"]/div/main/div/div[2]/div/div/div[1]/div[3]/div/div/div[2]/button')
element.click()
time.sleep(3)

time.sleep(3)


