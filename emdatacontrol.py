# -*- coding: utf-8 -*-
# ======================================
# 
# 電子マネー管理システム
# 対象データ自動取得制御メインモジュール
# 処理対象の会社売上データ(TOAMAS)を自動取得し
# 売上集計帳票を出力の準備をする
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
from datetime import datetime
import datetime
import os
import yaml
from emdbclass import DataBaseClass
import shutil
from emwebdataget import Webdataget

#################################################################
# メイン
#################################################################
if __name__ == "__main__":    
    # 基本情報取得
                
    #データベース操作クラス初期化及び共通パラメータyamlファイルから取得
    resdb = DataBaseClass() 
    
    #会社データ全件取得
    ret_rows = resdb.company_data_allget()
    
    # 共通パラメータ初期化
    web_data = []

    # web操作用yamlファイルから共通データ取得
    with open('C:/em/emproject/emoneyweb.yaml','r+',encoding="utf-8") as ry:
            config_yaml = yaml.safe_load(ry)
            web_data.append(config_yaml['dir_filepath']) 
            web_data.append(config_yaml['data_filepath'])
            web_data.append(config_yaml['data_name'])
            web_data.append(config_yaml['from_time'])
            web_data.append(config_yaml['to_time'])
            web_data.append(config_yaml['toamas_url1'])
            web_data.append(config_yaml['toamas_url2'])
            web_data.append(config_yaml['group_code'])
            web_data.append(config_yaml['account_code'])
            web_data.append(config_yaml['password'])
            web_data.append(config_yaml['logon_btn'])
            web_data.append(config_yaml['uri_btn'])
            web_data.append(config_yaml['income_btn'])
            web_data.append(config_yaml['inputopen_btn'])
            web_data.append(config_yaml['startdate_input'])
            web_data.append(config_yaml['enddate_input'])
            web_data.append(config_yaml['search_btn'])
            web_data.append(config_yaml['download_btn'])
    ########################################
    #
    # 会社データ毎の処理
    # 会社DBをシーケンスに読み、処理対象会社の売上明細データを自動取得
    # 会社データ　処理予定日 <= 処理日
    #
    ########################################        
    for i in range(0,len(ret_rows)):
        # 今日の日付と登録された処理予定日の比較
        t_date =  ret_rows[i][4]
        d = datetime.datetime.today()
        today = d.date()        
        td = today - t_date
        # TOAMASデータ利用会社であれば処理対象
        if ret_rows[i][9] == '2': 
        # 処理予定日<=今日なら処理対象とする
            if td.days >= 0:                
                print('*****************************************')
                print('対象会社 :',ret_rows[i][1])
                #debug
                print('対象データ自動取得開始 :',datetime.datetime.now())
                #class初期化
                reswdg = Webdataget(web_data,ret_rows[i])
                res = reswdg.webdataget()
                #ダウンロードしたファイルを規定のフォルダーに移す
                input_filepath = os.path.join(web_data[1],web_data[2])
                output_filepath = os.path.join(web_data[0],ret_rows[i][10])
                new_path = shutil.copy(input_filepath,output_filepath) 
                os.remove(input_filepath) 
        i += 1
    
    del resdb
    #print('ファイル取得終了：',datetime.datetime.now())            