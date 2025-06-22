# -*- coding: utf-8 -*-
# ======================================
# 
# 電子マネー管理システム
# 会社データの日付操作モジュール
# [環境]
#   Python 3.10.8
#   VSCode 1.64
#   <拡張>
#     |- Python  V2021.12
#     |- Pylance V2021.12
#
# [更新履歴]
#   2024/6/19  新規作成
#   2025/5/10  機能追加
#   
# ======================================
from datetime import datetime
import datetime
import yaml 
from emdbclass import DataBaseClass

#################################################################
# メイン
#################################################################
if __name__ == "__main__":    

    print('処理開始：',datetime.datetime.now()) 
    
    # 基本情報取得
    # 日付操作用yamlファイルから共通データ取得
    with open('C:/em/emproject/emdate.yaml','r+',encoding="utf-8") as dy:
            conf = yaml.safe_load(dy)
            #print(conf)
            com_arry = conf['companys']
    #データベース操作クラス初期化及び日付操作yamlファイルから取得した日付に更新
    #集計年・月の取得
    updatedate = input('本日以前の処理日を入力してください(yyyy/mm/dd):') 
    updatestartdate = input('処理日以前の処理開始日を入力してください(yyyy/mm/dd):') 
    updateenddate = input('処理終了日を入力してください(yyyy/mm/dd):') 
    
    resdb = DataBaseClass('1') 
    for com_no in com_arry:
        res = resdb.company_date_update(com_no, conf['updatedate'], conf['updatestartdate'], conf['updateenddate'])
            
    del resdb
    print('処理終了：',datetime.datetime.now())            