#################################################
#
#   営業提出資料
#   納品書データ取得
#   修理データ取得
#
#   指定期間に作成された納品書を取得し売上実績を把握
#
#   2024_1_24 新規作成
#   python 3.10.3
#
#################################################

import pyodbc as pyo
import openpyxl
from datetime import date

#ワークシートを事前にクリアする
wb = openpyxl.load_workbook(r'C:\Users\user\OneDrive\Workplace\2024年営業計画\wk_syuri.xlsx')
wb.remove(wb.worksheets[-1])
ws = wb.create_sheet(title="Sheet1")
wb.save(r'C:\Users\user\OneDrive\Workplace\2024年営業計画\wk_syuri.xlsx')

###################################
# 修理伝票データを日付で抽出
###################################
con_str2 = (
	r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};' 
    r'C:\Users\user\Desktop\修理伝票データベースVr.1.3元データリンク版 - 2023 - .mdb;'
    # r'Z:\データベース\修理伝票\元データリンク版\修理伝票データベースVr.1.3元データリンク版 - 2023 - .mdb;'
    # r'\\SERVER-TOKYO\社内共有フォルダ\データベース\修理伝票\元データリンク版\修理伝票データベースVr.1.3元データリンク版 - 2023 - .mdb;'
	)
###################################
# 指定日付はSQL文を変更
###################################
sql2 = 'SELECT * FROM ( 修理表 \
        LEFT JOIN 受付表 \
        ON(修理表.受付No = 受付表.受付No)) \
        LEFT JOIN ゴルフ場名簿 \
        ON(受付表.ゴルフ場No = ゴルフ場名簿.ゴルフ場No) \
        WHERE 発行日 Between #2024/05/01# AND #2024/05/31#'

con = pyo.connect(con_str2)
cursor = con.cursor()

rows_hosyu = cursor.execute(sql2).fetchall()

rows_hosyu_len = len(rows_hosyu)

print('修理伝票抽出処理開始')

#wb = openpyxl.load_workbook(r'C:\Users\user\OneDrive\Workplace\2024年営業計画\売上計画案（東京本社）.xlsx')
wb = openpyxl.load_workbook(r'C:\Users\user\OneDrive\Workplace\2024年営業計画\wk_syuri.xlsx')
sh_hosyu = wb['Sheet1']
rowno = sh_hosyu.max_row + 1
start_rowno = rowno

data_no = 0
for data_no in range(0, rows_hosyu_len):
    if rows_hosyu[data_no].総合計 != None:
        if rows_hosyu[data_no].総合計 != 0:
            wh_date = date(int(rows_hosyu[data_no].発行日.year), int(rows_hosyu[data_no].発行日.month), int(rows_hosyu[data_no].発行日.day))
            sh_hosyu.cell(rowno,1).value = wh_date
            ws_date = date(int(rows_hosyu[data_no].修理日.year), int(rows_hosyu[data_no].修理日.month), int(rows_hosyu[data_no].修理日.day))
            sh_hosyu.cell(rowno,2).value = ws_date
            sh_hosyu.cell(rowno,3).value = rows_hosyu[data_no].ゴルフ場No
            sh_hosyu.cell(rowno,4).value = rows_hosyu[data_no].ゴルフ場名
            sh_hosyu.cell(rowno,5).value = rows_hosyu[data_no].作業内容
            sh_hosyu.cell(rowno,6).value = rows_hosyu[data_no].総合計 
            sh_hosyu.cell(rowno,7).value = wh_date.year
            sh_hosyu.cell(rowno,8).value = wh_date.month
            sh_hosyu.cell(rowno,9).value = 20
            sh_hosyu.cell(rowno,11).value = 400
            rowno += 1

#wb.save(r'C:\Users\user\OneDrive\Workplace\2024年営業計画\売上計画案（東京本社）.xlsx')
wb.save(r'C:\Users\user\OneDrive\Workplace\2024年営業計画\wk_syuri.xlsx')

cursor.close()
con.close()