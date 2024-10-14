# -*- coding: utf-8 -*-
# ======================================
# 
# 電子マネー管理システム
# GUI版 レポート出力モジュール
# 売上集計帳票を出力
# [環境]
#   Python 3.10.3
#   
#
# [更新履歴]
#
#########################################
from emmonthsyubetu import dbMonthsyubetu
from emmonthkinsyu import dbMonthkinsyu
from emjikanreport import dbJikanReport
from emsyubetureport import dbSyubetuReport
from emplacereport import  dbPlaceReport
from emkinsyureport import dbKinsyuReport
from empdfconv import dbPdfConv
#from emzipfile import Zipfilecreate
from emdbclass import DataBaseClass
from datetime import datetime
import datetime
import os

#################################################################
# メイン
#################################################################
class Reportcontrol:
    def __init__(self, company_id, start_date, end_date):
        self.companycd_id = company_id
        self.start_date = start_date
        self.end_date = end_date    

        print('レポート出力処理開始：',datetime.datetime.now()) 
    
        # 基本情報取得                
        #データベース操作クラス初期化及び共通パラメータyamlファイルから取得
        self.resdb = DataBaseClass('1') 
    
        #対象会社データ取得
        ret_rows = self.resdb.company_data_get(self.companycd_id)
        self.SYEAR = self.start_date.year
        self.SMONTH = self.start_date.month
        self.SDAY = self.start_date.day
        self.EYEAR = self.end_date.year
        self.EMONTH = self.end_date.month
        self.EDAY = self.end_date.day  
        self.prec = ret_rows[0][2]
        self.block = ret_rows[0][3]

        #出力先パスの生成
        parm_data = self.resdb.init_return()
        self.dir_date = str(self.companycd_id) + '_'+str(self.SYEAR)+str(self.SMONTH)+str(self.SDAY)+'_'+str(self.EYEAR)+str(self.EMONTH)+str(self.EDAY)
        self.dir_out_filepath = os.path.join(parm_data[0], self.companycd_id, self.dir_date)     
        # ディレクトリー存在チェック
        if os.path.exists(self.dir_out_filepath):
            pass
        else:
            os.mkdir(self.dir_out_filepath) 
        #出力Excelファイル名＋フォルダー設定      
        self.excel_file =  str(self.companycd_id) + '_'+str(self.SYEAR)+str(self.SMONTH)+str(self.SDAY)+'_'+str(self.EYEAR)+str(self.EMONTH)+str(self.EDAY)+'.xlsx'
        self.file_out_path = os.path.join(self.dir_out_filepath, self.excel_file)
        #気象データの更新                
        res_list1 = self.resdb.weather_data_output(self.prec,self.block,self.SYEAR,self.SMONTH)
        #debug
        print(f'気象データ削除１件数：{res_list1[1]} 出力件数：{res_list1[0]}')
        #debug
        #年跨ぎ、月跨ぎの場合
        if (self.SYEAR != self.EYEAR) or (self.SMONTH != self.EMONTH) :
            res_list2 = self.resdb.weather_data_output(self.prec,self.block,self.EYEAR,self.EMONTH)
            #debug
            print(f'気象データ削除２件数：{res_list2[1]} 出力件数：{res_list2[0]}')
        
        #帳票作成用気象データ取得
        self.sdtime = datetime.datetime(self.SYEAR,self.SMONTH,self.SDAY,0,0,0)
        self.edtime = datetime.datetime(self.EYEAR,self.EMONTH,self.EDAY,0,0,0)
        self.ret_weather = self.resdb.weather_get3(self.sdtime, self.edtime, self.prec, self.block)
    
    def report_output(self):
        #共通：売上履歴データ取得
        df_paylog = self.resdb.paylog_get(self.companycd_id, self.start_date, self.end_date)
        df_sum_paylog = self.resdb.paylog_sum_get(self.companycd_id, self.end_date)
        
        #決済種別別売上集計
        print('決済種別別売上集計処理開始      :',datetime.datetime.now())
        df_syubetu = self.resdb.syubetsu_get()
        ressyubetu = dbSyubetuReport(df_syubetu, df_paylog, self.file_out_path, self.sdtime, self.edtime)
        ret_syubetu = ressyubetu.print_syubetsu()
        del ressyubetu
        
        #設置場所別売上集計
        print('設置場所別売上集計処理開始      :',datetime.datetime.now())
        # 現金分
        df_paylog1 = df_paylog[df_paylog['paykbncd'] == '1']
        if len(df_paylog1) > 0:
            resplace = dbPlaceReport(df_paylog, self.file_out_path, '1', self.sdtime, self.edtime)
            ret_place = resplace.print_place()
            del resplace
        # 電子決済分
        df_paylog2 = df_paylog[df_paylog['paykbncd'] == '2']
        if len(df_paylog2) > 0:
            resplace = dbPlaceReport(df_paylog, self.file_out_path, '2', self.sdtime, self.edtime)
            ret_place = resplace.print_place()
            del resplace
        
        #金種別売上集計
        print('金種別売上集計処理開始      :',datetime.datetime.now())
        # 現金分
        df_paylog1 = df_paylog[df_paylog['paykbncd'] == '1']
        if len(df_paylog1) > 0:
            reskinsyu = dbKinsyuReport(df_paylog, self.file_out_path, '1', self.sdtime, self.edtime)
            ret_kinsyu = reskinsyu.print_kinsyu()
            del reskinsyu
        # 電子決済分
        df_paylog2 = df_paylog[df_paylog['paykbncd'] == '2']
        if len(df_paylog2) > 0:
            reskinsyu = dbKinsyuReport(df_paylog, self.file_out_path, '2', self.sdtime, self.edtime)
            ret_kinsyu = reskinsyu.print_kinsyu()
            del reskinsyu
        
        #時間別売上集計
        print('時間別売上集計処理開始      :',datetime.datetime.now())
        # 現金分
        df_paylog1 = df_paylog[df_paylog['paykbncd'] == '1']
        if len(df_paylog1) > 0:
            resjikan = dbJikanReport(df_paylog, self.file_out_path, '1', self.sdtime, self.edtime, self.ret_weather)
            ret_jikan = resjikan.print_jikan()
            del resjikan
        # 電子決済分
        df_paylog2 = df_paylog[df_paylog['paykbncd'] == '2']
        if len(df_paylog2) > 0:
            resjikan = dbJikanReport(df_paylog, self.file_out_path, '2', self.sdtime, self.edtime, self.ret_weather)
            ret_jikan = resjikan.print_jikan()
            del resjikan
        
        #月別決済種別売上集計
        print('月別決済種別売上集計処理開始      :',datetime.datetime.now())        
        # 電子決済分
        resmonth = dbMonthsyubetu(df_syubetu, df_sum_paylog, self.file_out_path, '2', self.sdtime, self.edtime)
        ret_month = resmonth.print_monthly()
        del resmonth
        
        #月別金種別売上集計
        print('月別金種別売上集計処理開始      :',datetime.datetime.now())
        # 現金分
        df_sum_paylog1 = df_sum_paylog[df_sum_paylog['paykbncd'] == '1']
        if len(df_paylog1) > 0:
            resprice = dbMonthkinsyu(df_sum_paylog, self.file_out_path, '1', self.sdtime, self.edtime)
            ret_price = resprice.print_pricemonthly()
            del resprice
        # 電子決済分
        df_sum_paylog2 = df_sum_paylog[df_sum_paylog['paykbncd'] == '2']
        if len(df_paylog2) > 0:
            resprice = dbMonthkinsyu(df_sum_paylog, self.file_out_path, '2', self.sdtime, self.edtime)
            ret_price = resprice.print_pricemonthly()
            del resprice
        
        #PDFファイル作成
        print('PDFファイル作成処理開始      :',datetime.datetime.now())
        respdf = dbPdfConv(self.file_out_path, self.dir_out_filepath)
        ret_respdf = respdf.pdfconv()
        del respdf
        
        del self.resdb

        print('レポート出力処理終了：',datetime.datetime.now())   


        
                  