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
#import pygetwindow as pgw
import subprocess as sub
from emdbclass import DataBaseClass
import time


class Guidataget:
    def __init__(self,company_id):
        #データベース操作クラス初期化及び共通パラメータyamlファイルから取得
        resdb = DataBaseClass() 

        res_data = resdb.company_data_get(company_id)
        self.start_year = res_data[0][7].year
        self.start_month = res_data[0][7].month
        self.start_day = res_data[0][7].day
        self.end_year = res_data[0][8].year
        self.end_month = res_data[0][8].month
        self.end_day = res_data[0][8].day

        del resdb

        # Debug
        # self.start_year = 2024
        # self.start_month = 8
        # self.start_day = 5
        # self.end_year = 2024
        # self.end_month = 8
        # self.end_day = 11
    ##########################################
    #
    # かぞえもん 自動起動～ログイン～対象データ取得
    #
    #########################################
    def guiauto(self):
        time.sleep(5)
        # かぞえもん起動
        pro = sub.Popen('exec C:\SOFTLINK\売上照会サービス\ASMO.exe', shell=True)

        time.sleep(10)

        #window = pgw.getActiveWindow()
        # print('windw title = ',window.title)
        # print('window width =', window.width)
        # print('window height =', window.height)
        # print('window top =', window.top)
        # print('window left =' ,window.left)
        # print('window box =', window.box)
        # print('window center =', window.center)

        # 担当者IDを入力
        pag.write('9999999999')
        # パスワードを入力
        pag.moveTo(963, 569) 
        pag.click()
        pag.write('KW708kiwa')
        # ログインボタン押下
        pag.moveTo(844, 675) 
        pag.click()

        time.sleep(5)
        # メニューボタンを押す
        pag.moveTo(234, 51) 
        pag.click()

        time.sleep(5)

        # 売上明細csv出力を押す
        pag.moveTo(394, 335) 
        pag.click()
        time.sleep(3)

        # 日付範囲を指定を押す
        pag.moveTo(1119, 599) 
        pag.click()
        time.sleep(3)

        # 開始年を入力
        pag.click(1286, 648) 
        pag.write(str(self.start_year))
        time.sleep(1)

        # 開始月を入力
        pag.click(1344, 648) 
        pag.write(str(self.start_month))
        time.sleep(1)

        # 開始日を入力
        pag.click(1388, 648) 
        pag.write(str(self.start_day))
        time.sleep(1)

        # 終了年を入力
        pag.click(1286, 690) 
        pag.write(str(self.end_year))
        time.sleep(1)

        # 終了月を入力
        pag.click(1344, 690) 
        pag.write(str(self.end_month))
        time.sleep(1)

        # 終了日を入力
        pag.click(1388, 690) 
        pag.write(str(self.end_day))
        time.sleep(1)

        # 決定を押す
        pag.moveTo(845, 865) 
        pag.click()
        time.sleep(6)

        # csv出力を押す
        pag.moveTo(300, 142) 
        pag.click()
        time.sleep(1)
        # ファイル名入力
        pag.press('del')
        pag.write('uriagemeisai.csv')
        # 保存を押す
        pag.moveTo(912, 777) 
        pag.click()
        time.sleep(1)
        # 同じファイルを入れ替える'はい'を押す
        pag.moveTo(1019, 586) 
        pag.click()
        time.sleep(20)

        pro.kill()
        return 0





