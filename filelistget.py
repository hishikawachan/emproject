##########################################
#
#   営業提出資料
#   見積書データ取得
#   
#   指定期間に作成された見積書のタイトルを取得
#   
#   2024_1_25 新規作成
#   python 3.10.3
#
##########################################

import os
from datetime import datetime, date
import openpyxl

wb = openpyxl.load_workbook(r'C:\Users\user\OneDrive\Workplace\2024年営業計画\売上計画案（東京本社）.xlsx')
sh_jyutyu = wb['受注見込']
rowno = sh_jyutyu.max_row + 1

outcount = 0
file_dir = r'Z:\見積書'
input_fromdate = datetime(2023,11,1,0,0,0)
input_todate = datetime(2024,1,31,0,0,0)
# 
for file in os.listdir(file_dir):
    base, ext = os.path.splitext(file)
    if ext == '.xlsx' or ext == '.xls':
        file_path = os.path.join(file_dir, file)      
        file_info = os.stat(file_path)
        create_date = datetime.fromtimestamp(file_info.st_ctime)
        update_date = datetime.fromtimestamp(file_info.st_mtime)
        if create_date >= input_fromdate:
            if create_date <= input_todate:
                sh_jyutyu.cell(rowno,1).value = base
                sh_jyutyu.cell(rowno,2).value = date(int(create_date.year), int(create_date.month), int(create_date.day))
                sh_jyutyu.cell(rowno,3).value = date(int(update_date.year), int(update_date.month), int(update_date.day))
                rowno += 1
                outcount += 1

print('出力件数', outcount)
wb.save(r'C:\Users\user\OneDrive\Workplace\2024年営業計画\売上計画案（東京本社）.xlsx')