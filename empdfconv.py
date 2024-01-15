# -*- coding: utf-8 -*-
# ======================================
# 電子マネー管理システム
# MariaデータベースからデータExcel及びPDF出力
# PDFファイル作成
# [環境]20
#   Python 3.10.8
#   VSCode 1.64
#   <拡張>
#     |- Python  V2021.12
#     |- Pylance V2021.12
#
# [更新履歴]
#   2023/11/6  新規作成
# ======================================
from datetime import datetime
import datetime
import xlwings as xw
import glob

####
# 初期処理
####
class dbPdfConv:        
    # クラス初期化
    def __init__(self, excel_file, file_out_path):  
        
        # クラス初期化 
        self.file_out_path = file_out_path
        self.excel_file = excel_file
    #
    # 出力されたEXCELシートをxlwungsを使ってPDF変換する
    #     
    def pdfconv(self):
        #debug
        print('PDFファイル出力開始：',datetime.datetime.now())
        # pdfへの変換
        output_path = self.file_out_path + '/'
        #Excelファイルを取得
        excel_file =  glob.glob(self.excel_file) 

        App = xw.App(visible=False)        

        wb = xw.Book(excel_file[0])
        for j in wb.sheets:
            wb.sheets[j].to_pdf(path= output_path + j.name + '.pdf')   
        wb.close()
      
        App.quit()
        
        #debug
        print('PDFファイル出力終了：',datetime.datetime.now())