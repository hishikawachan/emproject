# -*- coding: utf-8 -*-
# ======================================
# 
# 電子マネー管理システム
# 月別会社別売上集計記録モジュール
# 処理対象の会社売上データ(DB)を指定月別に集計して
# チェックリストに記録する
# [環境]
#   Python 3.10.3
#   VSCode 1.64
#   <拡張>
#     |- Python  V2021.12
#     |- Pylance V2021.12
#
# [更新履歴]
#   2025/2/10  新規作成
#   
# ======================================
from datetime import datetime
import datetime
import yaml
from emdbclass import DataBaseClass
import openpyxl 
#################################################################
# メイン
#################################################################
if __name__ == "__main__":    
    
    print('集計開始：',datetime.datetime.now())  
                
    #データベース操作クラス初期化
    resdb = DataBaseClass('0') 

    # 共通yamlファイルから共通データ取得
    with open('C:/em/emproject/emoneyweb.yaml','r+',encoding="utf-8") as ry:
        config_yaml = yaml.safe_load(ry)
        check_list = config_yaml['data_check_list']

    # 集計データチェックリスト更新の準備
    wb = openpyxl.load_workbook(f'{check_list}')
    sh = wb.worksheets[0]
    # エリアをクリア
    mrow = sh.max_row
    mcol = sh.max_column
    # 実施日入力エリアの指定・セット
    cell_date = sh.cell(3, mcol + 1)
    cell_date.value = str(datetime.date.today())
    # 集計チェックリスト閉じる
    wb.save(f'{check_list}')

    #集計年・月の取得
    year = input('対象年を入力してください(数字4桁):') 
    month = input('対象月を入力してください(数字2桁以内):') 

    # DBから集計値を取得
    res_monthsum = resdb.paylog_monthsum_get(year,month)

    # 集計チェックリストに取得した集計値をセット
    wb = openpyxl.load_workbook(f'{check_list}')
    sh = wb.worksheets[0]
    for i in range(0,len(res_monthsum)):
        for x in range(4,int(mrow)):
            if sh.cell(x,1).value == res_monthsum[i][0]: #会社コード一致
                sh.cell(x,mcol+1).value = res_monthsum[i][2]
                break
    # 集計チェックリスト閉じる
    wb.save(f'{check_list}')

    print('集計終了：',datetime.datetime.now()) 