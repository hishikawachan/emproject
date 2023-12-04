# -*- coding: utf-8 -*-
# ======================================
# 
# 電子マネー管理システム
# 月報制御メインモジュール
# 処理対象の会社に対してDBへデータ出力
# 売上集計帳票を出力
# [環境]
#   Python 3.10.8
#   VSCode 1.64
#   <拡張>
#     |- Python  V2021.12
#     |- Pylance V2021.12
#
# [更新履歴]
#   2023/11/28  新バージョン作成
# ======================================
from datetime import datetime
import datetime
import os
import calendar
from emdbclass import DataBaseClass
from emsyubetureport import dbSyubetuReport
from emplacereport import dbPlaceReport
from emkinsyureport import dbKinsyuReport
from emjikanreport import dbJikanReport
from empdfconv import dbPdfConv
#################################################################
# 共通パラメータ
#################################################################
parm_data = []

#################################################################
# メイン
#################################################################
if __name__ == "__main__":    

    print('処理開始：',datetime.datetime.now()) 
    
    dt_now = datetime.datetime.now()
    print('月次帳票出力処理開始：',dt_now) 
    
    input_symd = input('処理日を入力(yyyyMMdd 99999999は終了):') 
    
    if input_symd != '99999999':
        year = int(input_symd[0:4])
        month = int(input_symd[4:6]) - 1        
        s_day = 1
        
        if month <= 0:
            month = 12
            year = year - 1 
        e_day = calendar.monthrange(year, month)[1]
        
        print('%s 年 %s 月の処理を行います' % (year,month)) 
    
        month_sdate = datetime.date(year, month, s_day)
        month_edate = datetime.date(year, month, e_day)
        flg = '1'
    else:
        flg = '0'
                
    #データベース操作クラス初期化及び共通パラメータyamlファイルから取得
    resdb = DataBaseClass() 
    
    #会社データ全件取得
    ret_rows = resdb.company_data_allget()
    
    ########################################
    #
    # 会社データ毎の処理
    # 会社DBをシーケンスに読み、処理対象の会社を検知したら帳票出力を行う
    #
    ########################################        
    for i in range(0,len(ret_rows)):
        # 今日の日付と登録された処理予定日の比較
        # t_date =  ret_rows[i][4]
        # d = datetime.datetime.today()
        # today = d.date()        
        # td = today - t_date
        # 処理予定日<=今日なら処理対象とする
        #if td.days >= 0:
        if flg == '1':            
            print('*****************************************')
            print('対象会社 :',ret_rows[i][1])
            #debug
            #print('対象データDB化開始 :',datetime.datetime.now())
        
            #parm_data = []
            #data_cnt = 0
            #共通パラメータセット
            #start_date = ret_rows[i][7]  #更新開始日セット
            #end_date   = ret_rows[i][8]  #更新終了日セット
            start_date = month_sdate      #更新開始日セット
            end_date   = month_edate      #更新終了日セット
            com_code = ret_rows[i][0]     #対象会社コード
            
            # 入力ファイルデータをDBに書き出し        
            # if ret_rows[i][9] == '1': #売上明細ファイル
            #     #debug
            #     print('売上明細処理開始 :',datetime.datetime.now())      
            #     ret = resdb.uriagemeisai_output(com_code, start_date, end_date, ret_rows[i][10])
            #     #debug
            #     print('売上明細処理終了 :',datetime.datetime.now())      
            # else:
            #     #debug
            #     print('TOAMAS処理開始 :',datetime.datetime.now()) 
            #     ret = resdb.income_output(com_code, start_date, end_date, ret_rows[i][10])
            #     #debug
            #     print('TOAMAS処理終了 :',datetime.datetime.now()) 
                
            # #debug
            # print('対象データDB化終了 :',datetime.datetime.now())

            #if int(ret[1]) > 0: #データの書き込み件数1件でもあれば
            if flg == '1':             
                SYEAR = start_date.year
                SMONTH = start_date.month
                SDAY = start_date.day
                EYEAR = end_date.year
                EMONTH = end_date.month
                EDAY = end_date.day
                companycd = ret_rows[i][0]        
                prec = ret_rows[i][2]
                block = ret_rows[i][3]
                #出力先パスの生成
                parm_data = resdb.init_return()
                dir_date = str(companycd) + '_'+str(SYEAR)+str(SMONTH)+str(SDAY)+'_'+str(EYEAR)+str(EMONTH)+str(EDAY)
                dir_out_filepath = os.path.join(parm_data[0], companycd, dir_date)     
                # ディレクトリー存在チェック
                if os.path.exists(dir_out_filepath):
                    pass
                else:
                    os.mkdir(dir_out_filepath) 
                #出力Excelファイル名＋フォルダー設定      
                excel_file =  str(companycd) + '_'+str(SYEAR)+str(SMONTH)+str(SDAY)+'_'+str(EYEAR)+str(EMONTH)+str(EDAY)+'.xlsx'
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
                
                #帳票作成用気象データ取得
                sdtime = datetime.datetime(SYEAR,SMONTH,SDAY,0,0,0)
                edtime = datetime.datetime(EYEAR,EMONTH,EDAY,0,0,0)
                ret_weather = resdb.weather_get3(sdtime, edtime, prec, block)
                
                #帳票作成処理
                #debug  
                print('帳票作成処理開始      :',datetime.datetime.now())
                
                #共通：売上履歴データ取得
                df_paylog = resdb.paylog_get(companycd, start_date, end_date)
                df_sum_paylog = resdb.paylog_sum_get(companycd, end_date)
                
                #決済種別別売上集計
                print('決済種別別売上集計処理開始      :',datetime.datetime.now())
                df_syubetu = resdb.syubetsu_get()
                ressyubetu = dbSyubetuReport(df_syubetu, df_paylog, file_out_path, sdtime, edtime)
                ret_syubetu = ressyubetu.print_syubetsu()
                del ressyubetu
                
                #設置場所別売上集計
                print('設置場所別売上集計処理開始      :',datetime.datetime.now())
                # 現金分
                df_paylog1 = df_paylog[df_paylog['paykbncd'] == '1']
                if len(df_paylog1) > 0:
                    resplace = dbPlaceReport(df_paylog, file_out_path, '1', sdtime, edtime)
                    ret_place = resplace.print_place()
                    del resplace
                # 電子決済分
                df_paylog2 = df_paylog[df_paylog['paykbncd'] == '2']
                if len(df_paylog2) > 0:
                    resplace = dbPlaceReport(df_paylog, file_out_path, '2', sdtime, edtime)
                    ret_place = resplace.print_place()
                    del resplace
                
                #金種別売上集計
                print('金種別売上集計処理開始      :',datetime.datetime.now())
                # 現金分
                df_paylog1 = df_paylog[df_paylog['paykbncd'] == '1']
                if len(df_paylog1) > 0:
                    reskinsyu = dbKinsyuReport(df_paylog, file_out_path, '1', sdtime, edtime)
                    ret_kinsyu = reskinsyu.print_kinsyu()
                    del reskinsyu
                # 電子決済分
                df_paylog2 = df_paylog[df_paylog['paykbncd'] == '2']
                if len(df_paylog2) > 0:
                    reskinsyu = dbKinsyuReport(df_paylog, file_out_path, '2', sdtime, edtime)
                    ret_kinsyu = reskinsyu.print_kinsyu()
                    del reskinsyu
                
                #時間別売上集計
                print('時間別売上集計処理開始      :',datetime.datetime.now())
                # 現金分
                df_paylog1 = df_paylog[df_paylog['paykbncd'] == '1']
                if len(df_paylog1) > 0:
                    resjikan = dbJikanReport(df_paylog, file_out_path, '1', sdtime, edtime, ret_weather)
                    ret_jikan = resjikan.print_jikan()
                    del resjikan
                # 電子決済分
                df_paylog2 = df_paylog[df_paylog['paykbncd'] == '2']
                if len(df_paylog2) > 0:
                    resjikan = dbJikanReport(df_paylog, file_out_path, '2', sdtime, edtime, ret_weather)
                    ret_jikan = resjikan.print_jikan()
                    del resjikan
                
                #月別決済種別売上集計
                # print('月別決済種別売上集計処理開始      :',datetime.datetime.now())
                
                # # 電子決済分
                # resmonth = dbMonthReport(df_syubetu, df_sum_paylog, file_out_path, '2', sdtime, edtime)
                # ret_month = resmonth.print_monthly()
                # del resmonth
                
                # #月別金種別売上集計
                # print('月別金種別売上集計処理開始      :',datetime.datetime.now())
                # 現金分
                # df_sum_paylog1 = df_sum_paylog[df_sum_paylog['paykbncd'] == '1']
                # if len(df_paylog1) > 0:
                #     resprice = dbPriceReport(df_sum_paylog, file_out_path, '1', sdtime, edtime)
                #     ret_price = resprice.print_pricemonthly()
                #     del resprice
                # # 電子決済分
                # df_sum_paylog2 = df_sum_paylog[df_sum_paylog['paykbncd'] == '2']
                # if len(df_paylog2) > 0:
                #     resprice = dbPriceReport(df_sum_paylog, file_out_path, '2', sdtime, edtime)
                #     ret_price = resprice.print_pricemonthly()
                #     del resprice
                
                #PDFファイル作成
                print('PDFファイル作成処理開始      :',datetime.datetime.now())
                respdf = dbPdfConv(file_out_path, dir_out_filepath)
                ret_respdf = respdf.pdfconv()
                del respdf
                
                #debug  
                print('帳票作成処理終了      :',datetime.datetime.now())                
                
                #対象会社データ更新日の更新
                res_row = resdb.company_updateday_update(companycd)
                            
        i += 1
    
    del resdb
    print('処理終了：',datetime.datetime.now())            