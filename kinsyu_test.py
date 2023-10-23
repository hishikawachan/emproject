# -*- coding: utf-8 -*-
# ======================================
# 
# 電子マネー管理システム
# 金種別時間別データ編集モジュール(テスト版)
# SQLを使ったデータ抽出
# [環境]
#   Python 3.8.9
#   VSCode 1.64
#   <拡張>
#     |- Python  V2021.12
#     |- Pylance V2021.12
#
# [更新履歴]
#   2023/9/16  新規作成
# ======================================
from datetime import datetime
import datetime
import yaml
import os 
from emoneydbclass import DataBaseClass
from emoneydbreportclass import dbReport
#################################################################
# 共通パラメータ
#################################################################
parm_data = []
SDATE = datetime.date(2023,  10, 2)
EDATE = datetime.date(2023, 10, 8)
COCODE = '0000004'
KBNCD = '2'
FPATH = r'C:/Users/hishi/em/emproject/src'
#################################################################
# メイン
#################################################################
if __name__ == "__main__":
    #
    # Configファイルから入力ファイル名等抽出    
    #
    # 共通パラメタ
    # [i]:dbip
    # [1]:dbname
    # [2]:dbport
    # [3]:dbuser
    # [4]:dbpassword
    # [5]:処理対象開始日
    # [6]:処理対象終了日
    # [7]:処理区分(1:売上明細 2:TOAMAS 3:ヤマトフィナンシャルデータ)
    # [8]:対象会社コード
    # [9]:帳票ファイル出力先ディレクトリ
    # 対象データリスト
    
    dt_now = datetime.datetime.now()
    print('処理開始：',dt_now) 
    
    # 基本情報取得
    with open('C:/Users/hishi/em/emproject/src/emoney.yaml','r+',encoding="utf-8") as ry:
        config_yaml = yaml.safe_load(ry)
        dbip = config_yaml['dbip']
        dbmarianame = config_yaml['dbmarianame']
        dbport = config_yaml['dbport']        
        dbuser = config_yaml['dbuser']
        dbpw = config_yaml['dbpw']
        parm_data.append(dbip)
        parm_data.append(dbmarianame)
        parm_data.append(dbport)        
        parm_data.append(dbuser)
        parm_data.append(dbpw)
        #file_path = config_yaml['dir_filepath']
        #parm_data.append(file_path)
        parm_data.append(FPATH)
        
        
        d = datetime.datetime.today()
        today = d.date()        
        #データベース操作クラス初期化
        resdb = DataBaseClass(parm_data) 
        
        parm_data = []
        parm_data.append(dbip)
        parm_data.append(dbmarianame)
        parm_data.append(dbport)        
        parm_data.append(dbuser)
        parm_data.append(dbpw)
        parm_data.append(SDATE)  #更新開始日セット
        parm_data.append(EDATE)  #更新終了日セット
        parm_data.append(KBNCD)  #処理区分セット
        parm_data.append(COCODE)  #対象会社コード
        parm_data.append(FPATH)  #ファイル出力先フォルダー
        
        resdbrep = dbReport(parm_data)
        res = resdbrep.main()
        
        
        
        
        #print('詳細データ件数',len(kinsyu_data))
        #print('金種別合計データ',sum_data)
        
    
            
            