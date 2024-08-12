##########################################
#
#   営業提出資料
#   見積書データ取得
#   
#   指定期間に作成された見積書のタイトル等を取得
#   
#   2024_1_25 新規作成
#   python 3.10.3
#
##########################################

import os
from datetime import datetime
import datetime
import openpyxl
import xlrd
#import pandas as pd

#################################
# 見積書データ抽出書き込み
#################################
def estselect(file_path, ext):
    # データをworkに書き出し
    wbw = openpyxl.load_workbook(r'C:\Users\user\OneDrive\Workplace\2024年営業計画\wk_book.xlsx')
    shw = wbw['Sheet1']
    rowno = shw.max_row + 1
    #colno = sh_jyutyu.max_column + 1
    try:     
        file_info = os.stat(file_path)
        wk_datetime1 = datetime.datetime.fromtimestamp(file_info.st_mtime)
        wk_datetime2 = datetime.date(wk_datetime1.year, wk_datetime1.month, wk_datetime1.day)            
        shw.cell(rowno,1).value = wk_datetime2
    except FileNotFoundError:
        print('ファイル情報が読み込めない ',file_path)
        #shw.cell(rowno,1).value = datetime(1900,1,1,0,0,0)
        return 8
    
    # エクセル　バージョン毎の処理
    if ext == '.xls':
        wb = xlrd.open_workbook(file_path)
        #print(f'FILE = {file_path} ')
        sh = wb.sheet_by_index(0)
        for row in range(0,26):
            for col in range(0,11):
                # # 日付
                # if row == 1 and col == 8:
                #     wk_date = sh.cell_value(row,col)
                # 社名
                if row == 2 and col == 0:
                     if sh.cell_value(row,col) != '':                      
                        shw.cell(rowno,3).value = sh.cell_value(row,col)
                if row == 3 and col == 0:
                     if sh.cell_value(row,col) != '':                      
                        shw.cell(rowno,3).value = sh.cell_value(row,col)
                if row == 4 and col == 0:
                     if sh.cell_value(row,col) != '':                      
                        shw.cell(rowno,3).value = sh.cell_value(row,col)
                
                # 見積番号(2箇所あり)
                if row == 2 and col == 10:
                    try:
                        shw.cell(rowno,2).value = sh.cell_value(row,col)
                    except IndexError:
                        shw.cell(rowno,2).value = '番号無'
                if row == 2 and col == 11:
                    try:
                        shw.cell(rowno,2).value = sh.cell_value(row,col)
                    except IndexError:
                        shw.cell(rowno,2).value = '番号無'
                # 金額
                if row == 8 and col == 2:
                     shw.cell(rowno,4).value = sh.cell_value(row,col)
                # 案件
                if row == 10 and col == 2:
                     shw.cell(rowno,5).value = sh.cell_value(row,col) 
                # ファイル
                shw.cell(rowno,6).value = file_path     
        #print(f'社名 = {wk_name} 見積番号= {wk_number} 金額 = {wk_kingaku} 案件= {wk_anken}')

    if ext == '.xlsx':
        try:
            wbm = openpyxl.load_workbook(file_path,data_only=True)
            #wbm = openpyxl.load_workbook(file_path)
            shm = wbm.worksheets[0] #最初のシートのみ対象とする
            #print(f'FILE(xlsx) = {file_path} ')
        except FileNotFoundError:
            print('ファイルが読み込めない(xlsx) = ',file_path)   
            return 9
        for row in range(1,27):
            for col in range(1,12):
                # # 日付
                # if row == 1 and col == 8:
                #     wk_date = sh.cell_value(row,col)
                # 社名
                if row == 3 and col == 1:
                     if shm.cell(row,col).value != None:                      
                        shw.cell(rowno,3).value = shm.cell(row,col).value
                if row == 4 and col == 1:
                     if shm.cell(row,col).value != None:                      
                        shw.cell(rowno,3).value = shm.cell(row,col).value
                # 見積番号(2箇所あり)
                if row == 3 and col == 11:
                    try:
                        shw.cell(rowno,2).value = shm.cell(row,col).value
                    except IndexError:
                        shw.cell(rowno,2).value = '番号無'
                if row == 3 and col == 12:
                    try:
                        shw.cell(rowno,2).value = shm.cell(row,col).value
                    except IndexError:
                        shw.cell(rowno,2).value = '番号無'
                # 金額
                #if row == 8 and col == 3:
                #     shw.cell(rowno,5).value = shm.cell(row,col).value
                #print(f'金額(8,3)={shm.cell(8,3).value}')
                #print(f'金額(9,3)={shm.cell(9,3).value}')
                if row == 9 and col == 3:
                     shw.cell(rowno,4).value = shm.cell(row,col).value
                # 案件
                if row == 11 and col == 2:
                     shw.cell(rowno,5).value = shm.cell(row,col).value
                if row == 11 and col == 3:
                     shw.cell(rowno,5).value = shm.cell(row,col).value
                # ファイル
                shw.cell(rowno,6).value = file_path   
                 
        # ファイル閉じる
        wbm.save(file_path)
    
    
    #書き込んだデータを保存
    wbw.save(r'C:\Users\user\OneDrive\Workplace\2024年営業計画\wk_book.xlsx')
    return 0

#################################
# メイン
#################################
if __name__ == "__main__":
    outcount = 0
    file_dir = r'C:\Users\user\OneDrive\Workplace\2024年営業計画\売上予想データ'

    print('処理開始')

    #ワークシートを事前にクリアする
    wbw = openpyxl.load_workbook(r'C:\Users\user\OneDrive\Workplace\2024年営業計画\wk_book.xlsx')
    wbw.remove(wbw.worksheets[-1])
    wsw = wbw.create_sheet(title="Sheet1")
    wbw.save(r'C:\Users\user\OneDrive\Workplace\2024年営業計画\wk_book.xlsx')  
    # 見積ファイルごとの処理
    for file in os.listdir(file_dir):
        base, ext = os.path.splitext(file)
        if ext == '.xlsx' or ext == '.xls':
            file_path = os.path.join(file_dir, file) 
            res = estselect(file_path, ext)
            if res == 0:
                outcount += 1
            else:
                break

    print('出力件数', outcount)
