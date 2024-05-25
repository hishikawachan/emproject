# -*- coding: utf-8 -*-
# ======================================
# 
# 電子マネー管理システム
# 処理データWebから自動取得操作class　
# [環境]
#   Python 3.10.3
#   VSCode 1.64
#   <拡張>
#     |- Python  V2021.12
#     |- Pylance V2021.12
#
# [更新履歴]
#   2024/5/23  新規作成
#   
# ======================================
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import datetime
import os

class Webdataget:
    def __init__(self,web_data,company_data):
        self.dir_filepath = web_data[0] 
        self.data_filepath = web_data[1]
        self.data_name = web_data[2]
        self.from_time = web_data[3]
        self.to_time = web_data[4]
        self.toamas_url1 = web_data[5]
        self.toamas_url2 = web_data[6]
        self.group_code = web_data[7]
        self.account_code = web_data[8]
        self.password = web_data[9]
        self.logon_btn = web_data[10]
        self.uri_btn = web_data[11]
        self.income_btn = web_data[12]
        self.inputopen_btn = web_data[13]
        self.startdate_input = web_data[14]
        self.enddate_input = web_data[15]
        self.search_btn = web_data[16]
        self.download_btn = web_data[17]            
        
        self.fiename = company_data[10] #入力ファイル名
        self.groupcd = company_data[11] #所属コード
        self.accountcd = company_data[12] #アカウントコード
        self.key_password = company_data[13] #パスワード
        self.startday = company_data[7] #検索開始日
        self.endday = company_data[8] #検索終了日
        

##########################################
#
# TOAMAS 自動起動～ログイン～対象データ取得
#
#########################################
    def webdataget(self):
        print('ファイル取得開始',datetime.datetime.now())

        # Chrome Webドライバー の インスタンスを生成
        driver = webdriver.Chrome()

        # Webドライバーでログインページを起動
        #driver.get('https://toamas-amusement.thincacloud.com/Logon')
        driver.get(self.toamas_url1)
        time.sleep(1)

        #ログイン情報入力
        # 所属コード
        #driver.find_element(By.ID,"input-39").send_keys("0158")
        driver.find_element(By.ID,self.group_code).send_keys(self.groupcd)
        # アカウントID
        #driver.find_element(By.ID,"logon-id").send_keys("001144001001")
        driver.find_element(By.ID,self.account_code).send_keys(self.accountcd)
        # パスワード
        #driver.find_element(By.ID,"password").send_keys("KW708kiwa")
        driver.find_element(By.ID,self.password).send_keys(self.key_password)
        # ログオンボタン　クリック
        #element = driver.find_element(By.XPATH,'//*[@id="app"]/div[2]/div/form/div/div[3]/button')
        element = driver.find_element(By.XPATH,self.logon_btn)
        element.click()
        time.sleep(3)

        #各種メニュー画面に遷移
        #driver.get('https://toamas-amusement.thincacloud.com/')
        driver.get(self.toamas_url2)
        time.sleep(2)

        #インカム情報メニューを開く
        #element = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/header/div/div[3]/span[1]/button[1]/span/i')
        element = driver.find_element(By.XPATH,self.uri_btn)
        element.click()
        time.sleep(1)
        #element = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/nav[2]/div[1]/div[1]/div[1]/div/a')
        element = driver.find_element(By.XPATH,self.income_btn)
        element.click()
        time.sleep(2)

        #日時範囲入力を開く
        #element = driver.find_element(By.XPATH,'//*[@id="app"]/div/header/div/button/span/i')
        element = driver.find_element(By.XPATH,self.inputopen_btn)
        element.click()
        time.sleep(2)

        #検索日時情報を入力し、検索開始
        from_datetime = str(self.startday) + ' ' + str(self.from_time)
        to_datetime = str(self.endday) + ' ' + str(self.to_time)

        #driver.find_element(By.ID,"input-110").send_keys("2024-05-11 03:00")
        driver.find_element(By.XPATH,self.startdate_input).send_keys(from_datetime)
        time.sleep(2)
        #driver.find_element(By.ID,"input-118").send_keys("2024-05-20 23:00")
        driver.find_element(By.XPATH,self.enddate_input).send_keys(to_datetime)
        time.sleep(2)

        #element = driver.find_element(By.XPATH,'//*[@id="searchButtonArea"]/div/div/div[2]/button')
        element = driver.find_element(By.XPATH, self.search_btn)
        element.click()
        time.sleep(5)

        #検索したデータをダウンロードフォルダに保存
        #element = driver.find_element(By.XPATH,'//*[@id="app"]/div/main/div/div[2]/div/div/div[1]/div[3]/div/div/div[2]/button')
        element = driver.find_element(By.XPATH,self.download_btn)
        element.click()
        time.sleep(3)

        driver.quit()
        print('ファイル取得完了',datetime.datetime.now())
        return 0


