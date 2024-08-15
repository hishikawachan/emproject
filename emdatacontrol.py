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
from emguiauto import Guidataget
import openpyxl 

#################################################################
# メイン
#################################################################
if __name__ == "__main__":    
    
    print('ファイル取得開始：',datetime.datetime.now())   
                
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
            web_data.append(config_yaml['startdatetime_input'])
            web_data.append(config_yaml['enddatetime_input'])
            web_data.append(config_yaml['search_btn'])
            web_data.append(config_yaml['download_btn'])
            web_data.append(config_yaml['area_gether_btn'])
            web_data.append(config_yaml['gether_dropdown'])
            web_data.append(config_yaml['gether_dropdown_no'])
            web_data.append(config_yaml['startdate_input'])
            web_data.append(config_yaml['enddate_input'])
            web_data.append(config_yaml['gether_btn'])
            web_data.append(config_yaml['gether_num'])
            web_data.append(config_yaml['data_check_list'])
            check_list = config_yaml['data_check_list']
    # 集計データチェックリスト更新の準備
    wb = openpyxl.load_workbook(f'{check_list}')
    sh = wb.worksheets[0]
    # エリアをクリア
    mrow = sh.max_row
    mcol = sh.max_column
    #for i in range(3, mrow):
    #     cell = sh.cell(i, 5)
    #     cell.value = None
    # 実施日入力エリアの指定・セット
    cell_date = sh.cell(3, mcol + 1)
    cell_date.value = str(datetime.date.today())
    # 集計チェックリスト閉じる
    wb.save(f'{check_list}')
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
                print('データ取得対象会社 :',ret_rows[i][1])
                # 残っているダウンロードファイルがあれば削除
                input_filepath = os.path.join(web_data[1],web_data[2])
                if os.path.isfile(input_filepath):
                    os.remove(input_filepath) 
                # class初期化
                reswdg = Webdataget(web_data,ret_rows[i])
                # 売上明細データ自動取得 売上合計金額を返す
                total = reswdg.dataget()
                # ダウンロードしたファイルを規定のフォルダーに移す
                if total != -1:
                    input_filepath = os.path.join(web_data[1],web_data[2])
                    output_filepath = os.path.join(web_data[0],ret_rows[i][10])
                    new_path = shutil.copy(input_filepath,output_filepath) 
                    os.remove(input_filepath) 
                    # 売上集計チェックリストに合計金額(int化)をセット
                    wb = openpyxl.load_workbook(f'{check_list}')
                    sh = wb.worksheets[0]
                    for x in range(4,int(mrow)):
                        if sh.cell(x,1).value == ret_rows[i][0]: #会社コード一致
                            sh.cell(x,mcol+1).value = int(total.replace(',', ''))
                            #sh.cell(x,5).value = total
                            break
                    # 集計チェックリスト閉じる
                    wb.save(f'{check_list}')
                else:
                    print('検索対象データ無し',ret_rows[i][1])

        #i += 1
    
    del resdb

    # かぞえもんデータ取得class初期化
    resgui = Guidataget('0000004')
    # かぞえもんデータ自動取得
    res = resgui.guiauto()
    print('ファイル取得終了：',datetime.datetime.now())            