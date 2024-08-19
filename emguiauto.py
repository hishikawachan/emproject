# -*- coding: utf-8 -*-
# ======================================
# 
# 電子マネー管理システム
# かぞえもんデータ自動取得制御メインモジュール
# 処理対象の会社売上データ(かぞえもん)を自動取得し
# 売上集計帳票を出力の準備をする
# [環境]
#   Python 3.10.3
#   VSCode 1.64
#   <拡張>
#     |- Python  V2021.12
#     |- Pylance V2021.12
#
# [更新履歴]
#   2024/8/15  新規作成
#   
# ======================================
import pyautogui as pag
import pygetwindow as pgw
import subprocess as sub
import yaml
import time

class Guidataget:
    def __init__(self):        
        with open('C:/em/emproject/emoneyweb.yaml','r+',encoding="utf-8") as ry:
            config_yaml = yaml.safe_load(ry)
            self.idx = config_yaml['adress'][0]['x'] #担当者ID
            self.idy = config_yaml['adress'][0]['y'] 
            self.passx = config_yaml['adress'][1]['x'] #パスワード
            self.passy = config_yaml['adress'][1]['y'] 
            self.loginbx = config_yaml['adress'][2]['x'] #ログインボタン
            self.loginby = config_yaml['adress'][2]['y'] 
            self.menux = config_yaml['adress'][3]['x'] #メニューボタン
            self.menuy = config_yaml['adress'][3]['y'] 
            self.uricsvx = config_yaml['adress'][4]['x'] #売上明細csv出力
            self.uricsvy = config_yaml['adress'][4]['y'] 
            self.datebx = config_yaml['adress'][5]['x'] #日付範囲ラジオボタン            self.uricsvy = config_yaml['adress'][5]['y'] 
            self.dateby = config_yaml['adress'][5]['y'] 
            self.s_yearx = config_yaml['adress'][6]['x'] #検索開始年 
            self.s_yeary = config_yaml['adress'][6]['y'] 
            self.s_monthx = config_yaml['adress'][7]['x'] #検索開始月 
            self.s_monthy = config_yaml['adress'][7]['y'] 
            self.s_dayx = config_yaml['adress'][8]['x'] #検索開始日 
            self.s_dayy = config_yaml['adress'][8]['y'] 
            self.e_yearx = config_yaml['adress'][9]['x'] #検索終了年 
            self.e_yeary = config_yaml['adress'][9]['y'] 
            self.e_monthx = config_yaml['adress'][10]['x'] #検索終了月
            self.e_monthy = config_yaml['adress'][10]['y'] 
            self.e_dayx = config_yaml['adress'][11]['x'] #検索終了日
            self.e_dayy = config_yaml['adress'][11]['y'] 
            self.ketteix = config_yaml['adress'][12]['x'] #決定ボタン
            self.ketteiy = config_yaml['adress'][12]['y'] 
            self.csvoutx = config_yaml['adress'][13]['x'] #csv出力
            self.csvouty = config_yaml['adress'][13]['y'] 
            self.hozonx = config_yaml['adress'][14]['x'] #保存
            self.hozony = config_yaml['adress'][14]['y'] 
            self.haix = config_yaml['adress'][15]['x'] #保存
            self.haiy = config_yaml['adress'][15]['y'] 
            self.id = config_yaml['id'] #担当者ID
            self.passwd = config_yaml['passwd'] #担当者ID
            self.file_name = config_yaml['file_name'] #保存ファイル名
        
        self.start_year = input('検索開始年を入力(yyyy)') 
        self.start_month = input('検索開始月を入力(mm)') 
        self.start_day = input('検索開始日を入力(dd)') 
        self.end_year = input('検索終了年を入力(yyyy)') 
        self.end_month = input('検索終了月を入力(mm)') 
        self.end_day = input('検索終了日を入力(dd)') 
        self.waittime = input('プログラム終了待機時間を入力(ss)※週:20 月:80 処理終了:99 >>') 
        return self.waittime
    ##########################################
    #
    # かぞえもん 自動起動～ログイン～対象データ取得
    #
    #########################################
    def guiauto(self):
        time.sleep(2)
        # かぞえもん起動
        pro = sub.Popen('C:\SOFTLINK\売上照会サービス\ASMO.exe', shell=True)       

        time.sleep(2)

        # 初期画面出るまで待機
        window = pgw.getActiveWindow()
        while window.title != 'かぞえもん':
            pag.sleep(1)        
            window = pgw.getActiveWindow()
              
        # 担当者IDを入力
        window = pgw.getActiveWindow()
        #pag.click(x=self.idx, y=self.idy, clicks=1, button="primary")
        pag.sleep(5)
        pag.write(self.id)
        pag.sleep(2)
        # パスワードを入力
        pag.moveTo(self.passx, self.passy) 
        pag.click()
        pag.write(self.passwd)
        time.sleep(2)
        # ログインボタン押下
        pag.moveTo(self.loginbx, self.loginby) 
        pag.click()
        time.sleep(5)
        # メニューボタンを押す
        pag.moveTo(self.menux, self.menuy) 
        pag.click()
        time.sleep(5)
        # 売上明細csv出力を押す
        pag.moveTo(self.uricsvx, self.uricsvy) 
        pag.click()
        time.sleep(3)
        # 日付範囲を指定を押す
        pag.moveTo(self.datebx, self.dateby) 
        pag.click()
        time.sleep(3)
        # 開始年を入力
        pag.click(self.s_yearx, self.s_yeary) 
        pag.write(str(self.start_year))
        time.sleep(1)
        # 開始月を入力
        pag.click(self.s_monthx, self.s_monthy) 
        pag.write(str(self.start_month))
        time.sleep(1)
        # 開始日を入力
        pag.click(self.s_dayx, self.s_dayy) 
        pag.write(str(self.start_day))
        time.sleep(1)
        # 終了年を入力
        pag.click(self.e_yearx, self.e_yeary) 
        pag.write(str(self.end_year))
        time.sleep(1)
        # 終了月を入力
        pag.click(self.e_monthx, self.e_monthy) 
        pag.write(str(self.end_month))
        time.sleep(1)
        # 終了日を入力
        pag.click(self.e_dayx, self.e_dayy) 
        pag.write(str(self.end_day))
        time.sleep(1)
        # 決定を押す
        pag.moveTo(self.ketteix, self.ketteiy) 
        pag.click()
        time.sleep(3)
        # csv出力を押す
        pag.moveTo(self.csvoutx, self.csvouty) 
        pag.click()
        time.sleep(1)
        # ファイル名入力
        pag.press('del')
        pag.write(self.file_name)
        # 保存を押す
        pag.moveTo(self.hozonx, self.hozony) 
        pag.click()
        time.sleep(1)
        # 同じファイルを入れ替える'はい'を押す
        pag.moveTo(self.haix, self.haiy) 
        pag.click()
        time.sleep(int(self.waittime))

        pro.kill()
        return 0





