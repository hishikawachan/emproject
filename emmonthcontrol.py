# -*- coding: utf-8 -*-
# ======================================
# 
# 電子マネー管理システム
# 月次処理制御メインモジュール
# 登録されているすべての会社に対して月次帳票を出力する
# [環境]
#   Python 3.10.3
#   VSCode 1.64
#   <拡張>
#     |- Python  V2021.12
#     |- Pylance V2021.12
#
# [更新履歴]

from emmonthsyubetu import dbMonthsyubetu
from emmonthkinsyu import dbMonthkinsyu
from emjikanreport import dbJikanReport
from emsyubetureport import dbSyubetuReport
from emplacereport import  dbPlaceReport
from emkinsyureport import dbKinsyuReport
from empdfconv import dbPdfConv
from emzipfile import Zipfilecreate
from emdbclass import DataBaseClass
from datetime import datetime
import datetime
import calendar
import os
import yaml
import openpyxl 
#################################################################
# 共通パラメータ
#################################################################
parm_data = []

#################################################################
# メイン
#################################################################
if __name__ == "__main__":    

    print('月次処理開始：',datetime.datetime.now()) 
    
    # 基本情報取得                
    #データベース操作クラス初期化
    resdb = DataBaseClass('0') 

    # 共通yamlファイルから共通データ取得
    with open('C:\Users\hishi\OneDrive\Labo\em\emproject\yaml/emoneyweb.yaml','r+',encoding="utf-8") as ry:
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
    month = input('対象月を入力してください(数字1 ～ 12):') 

    #debug  
    print('月次売上集計処理・記録開始      :',datetime.datetime.now())

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

    #debug  
    print('月次売上集計処理・記録終了      :',datetime.datetime.now())


    #会社データ全件取得
    ret_rows = resdb.company_data_allget()

    # その月の日数を取得
    _, last_day_num = calendar.monthrange(int(year), int(month))

    # その月の最終日、初日を取得
    last_day = datetime.date(int(year), int(month), int(last_day_num))
    first_day = datetime.date(int(year), int(month), 1)

    #debug  
    print('帳票作成処理開始      :',datetime.datetime.now())

    # 月次帳票作成処理開始
    for i in range(0,len(ret_rows)):
        print('*****************************************')
        print('対象会社 :',ret_rows[i][1])
        parm_data = []
        data_cnt = 0
        #共通パラメータセット
        start_date = first_day  #処理開始日セット
        end_date   = last_day  #更新終了日セット
        com_code = ret_rows[i][0]    #対象会社コード

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
        #共通：売上履歴データ取得
        df_paylog = resdb.paylog_get(companycd, start_date, end_date)
        df_sum_paylog = resdb.paylog_sum_get(companycd, end_date)

        #対象データがある場合、帳票処理実行
        if len(df_paylog) > 0:
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
            print('月別決済種別売上集計処理開始      :',datetime.datetime.now())
            
            # 電子決済分
            resmonth = dbMonthsyubetu(df_syubetu, df_sum_paylog, file_out_path, '2', sdtime, edtime)
            ret_month = resmonth.print_monthly()
            del resmonth
            
            #月別金種別売上集計
            print('月別金種別売上集計処理開始      :',datetime.datetime.now())
            # 現金分
            df_sum_paylog1 = df_sum_paylog[df_sum_paylog['paykbncd'] == '1']
            if len(df_paylog1) > 0:
                resprice = dbMonthkinsyu(df_sum_paylog, file_out_path, '1', sdtime, edtime)
                ret_price = resprice.print_pricemonthly()
                del resprice
            # 電子決済分
            df_sum_paylog2 = df_sum_paylog[df_sum_paylog['paykbncd'] == '2']
            if len(df_paylog2) > 0:
                resprice = dbMonthkinsyu(df_sum_paylog, file_out_path, '2', sdtime, edtime)
                ret_price = resprice.print_pricemonthly()
                del resprice
            
            #PDFファイル作成
            print('PDFファイル作成処理開始      :',datetime.datetime.now())
            respdf = dbPdfConv(file_out_path, dir_out_filepath)
            ret_respdf = respdf.pdfconv()
            del respdf

            # 保存フォルダーの圧縮
            reszip = Zipfilecreate(parm_data[0], companycd, dir_date )
            files_no = reszip.filezip()                

    #debug  
    print('帳票作成処理終了      :',datetime.datetime.now())     