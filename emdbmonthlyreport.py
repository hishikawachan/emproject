# -*- coding: utf-8 -*-
# ======================================
# 
# 電子マネー管理システム
# 月次帳票出力メインモジュール　
# [環境]
#   Python 3.10.8
#   VSCode 1.64
#   <拡張>
#     |- Python  V2021.12
#     |- Pylance V2021.12
#
# [更新履歴]
#   2023/3/16  新規作成
#   2023/8/2   機能追加
#   2023/8/21  機能変更
# ======================================
from datetime import datetime
import datetime
import calendar
import datetime
import os 
from emdbclass import DataBaseClass
from emsyubetureport import dbSyubetuReport
from emplacereport import dbPlaceReport
from emkinsyureport import dbKinsyuReport
from emjikanreport import dbJikanReport
from emmonthreport import dbMonthReport
from empdfconv import dbPdfConv

#################################################################
# DB制御classに渡すパラメータ
#################################################################
parm_data = []

#################################################################
# メイン
#################################################################
if __name__ == "__main__":
    #
    # Configファイルから入力ファイル名等抽出    
    #
    # パラメタ
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
    # 
    # # 対象データリスト
    
    dt_now = datetime.datetime.now()
    print('月次帳票出力処理開始：',dt_now) 
    
    input_symd = input('処理日を入力(yyyyMMdd 99999999は終了):') 
    
    if input_symd != '99999999':
        year = int(input_symd[0:4])
        month = int(input_symd[4:6]) - 1
        #前月の初日と最終日を求める
        # d = datetime.datetime.today()
        # today = d.date()        
        # month = today.month - 1
        # year = today.year
        s_day = 1
        if month <= 0:
            month = 12
            year = year - 1 
        
        start_date = datetime.date(int(year), int(month), int(s_day))
        e_day = calendar.monthrange(year, month)[1]
        end_date = datetime.date(int(year), int(month), int(e_day))
        
        #データベース操作クラス初期化
        resdb = DataBaseClass() 
    
        #会社データ全件取得
        ret_rows = resdb.company_data_allget()
        
        for i in range(0,len(ret_rows)):
            
                
            print('対象会社 :',ret_rows[i][1])
            
            #共通パラメータセット
            com_code = ret_rows[i][0]    #対象会社コード         

            SYEAR = start_date.year
            SMONTH = start_date.month
            SDAY = start_date.day
            EYEAR = end_date.year
            EMONTH = end_date.month
            EDAY = end_date.day
       
            prec = ret_rows[i][2]
            block = ret_rows[i][3]
            #出力先パスの生成
            parm_data = resdb.init_return()
            dir_date = str(com_code) + '_'+str(SYEAR)+str(SMONTH)+str(SDAY)+'_'+str(EYEAR)+str(EMONTH)+str(EDAY)
            dir_out_filepath = os.path.join(parm_data[0], com_code, dir_date)     
            # ディレクトリー存在チェック
            if os.path.exists(dir_out_filepath):
                pass
            else:
                os.mkdir(dir_out_filepath) 
            #出力Excelファイル名＋フォルダー設定      
            excel_file =  str(com_code) + '_'+str(SYEAR)+str(SMONTH)+str(SDAY)+'_'+str(EYEAR)+str(EMONTH)+str(EDAY)+'.xlsx'
            file_out_path = os.path.join(dir_out_filepath, excel_file)
    
            #気象データの更新
            res_list1 = resdb.weather_data_output(prec,block,SYEAR,SMONTH)
            #debug
            print(f'気象データ削除１件数：{res_list1[1]} 出力件数：{res_list1[0]}')
            #debug
            #年跨ぎ、月跨ぎの場合
            if (SYEAR != EYEAR) or (SMONTH != EMONTH) :
                res_list2 = resdb.weather_data_output(prec,block,EYEAR,EMONTH)
                #debug
                print(f'気象データ削除２件数：{res_list2[1]} 出力件数：{res_list2[0]}')
                
            #帳票作成処理
            #debug  
            print('帳票作成処理開始      :',datetime.datetime.now())
            
            #共通：売上履歴データ取得
            df_paylog = resdb.paylog_get(com_code, start_date, end_date)
            df_sum_paylog = resdb.paylog_sum_get(com_code, end_date)
            
            #決済種別別売上集計
            df_syubetu = resdb.syubetsu_get()
            ressyubetu = dbSyubetuReport(df_syubetu, df_paylog, file_out_path)
            ret_syubetu = ressyubetu.print_syubetsu()
            del ressyubetu
            
            #設置場所別売上集計
            # 現金分
            resplace = dbPlaceReport(df_paylog, file_out_path, '1')
            ret_place = ressplace.print_place()
            del resplace
            # 電子決済分
            ressplace = dbPlaceReport(df_paylog, file_out_path, '2')
            ret_place = ressplace.print_place()
            del resplace
            
            #金種別売上集計
            # 現金分
            reskinsyu = dbKinsyuReport(df_paylog, file_out_path, '1')
            ret_kinsyu = reskinsyu.print_kinsyu()
            del reskinsyu
            # 電子決済分
            reskinsyu = dbKinsyuReport(df_paylog, file_out_path, '2')
            ret_kinsyu = reskinsyu.print_kinsyu()
            del reskinsyu
            
            #時間別売上集計
            # 現金分
            resjikan = dbJikanReport(df_paylog, file_out_path, '1')
            ret_jikan = reskinsyu.print_jikan()
            del resjikan
            # 電子決済分
            resjikan = dbJikanReport(df_paylog, file_out_path, '2')
            ret_jikan = reskinsyu.print_jikan()
            del resjikan
            
            #月別売上集計
            # 現金分
            resmonth = dbMonthReport(df_sum_paylog, file_out_path, '1')
            ret_month = resmonth.print_monthly()
            del resmonth
            # 電子決済分
            resmonth = dbMonthReport(df_sum_paylog, file_out_path, '2')
            ret_month = resmonth.print_monthly()
            del resmonth
            
            #PDFファイル作成
            respdf = dbPdfConv(file_out_path, dir_out_filepath)
            ret_respdf = respdf.pdfconv()
            del respdf
            
            #debug  
            print('帳票作成処理終了      :',datetime.datetime.now())       
        
dt_now = datetime.datetime.now()
print('月次帳票出力処理終了：',dt_now) 
        
       
        
        
        
        
        
        
        
        
        
        
