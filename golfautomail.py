# -*- coding: utf-8 -*-
# ======================================
# 
# 電子マネーバッチ送信モジュール
# 来場者リストを基に謝礼メールを送る
# 
# [環境]
#   Python 3.10.3
#   VSCode 1.64
#   <拡張>
#     |- Python  V2021.12
#     |- Pylance V2021.12
#
# [更新履歴]
#   2025/3/13  新規作成
#   
# ======================================
from datetime import datetime
from openpyxl import load_workbook

import datetime
import win32com.client
import time
#################################################################
# メイン
#################################################################
if __name__ == "__main__":    

    print('処理開始：',datetime.datetime.now())     

    #来場者リストロード
    wb = load_workbook(r'C:\Users\hishi\OneDrive\Workplace\2025年ジャパンゴルフフェア資料\2025年ゴルフフェア　来場者リスト.xlsx')
    ws = wb['来場者リスト']
    ws = wb.active

    ########################################
    #
    # 来場者データを1件ずつよみメールアドレスがある会社データ毎の処理
    #  
    # column = 4   : 氏名
    # column = 5   : 役職
    # column = 6   : 社名
    # column = 7   : 練習場名
    # column = 13  : メールアドレス
    ########################################    
    subject_org = '第59回ジャパンゴルフフェア2025 弊社ブースご来場の御礼'
    body1 = '貴社  益々ご清栄のこととお慶び申し上げます'
    body2 = 'この度は、「第59回ジャパンゴルフフェア2025」弊社ブースにご来場いただき、'
    body3 = 'ありがとうございました'
    body4 = 'お忙しい中、貴重なお時間をいただき厚く御礼を申し上げます'
    body5 = '多数のお客様に来場いただきました為説明など至らぬ点があったと感じております'
    body6 = '改めて御社にご挨拶に伺い、ご要望など承る機会をいただければと思っております'
    body7 = '今後、御社への訪問のお願いなどで連絡させていただきますが何卒よろしく'
    body8 = 'お願いいたします'
    body9 = 'それ以外にもご質問や追加の情報が必要な場合は、お気軽にお申しつけください'
    body10 = '改めまして、ご来場ありがとうございました'
    body11 = '今後とも何卒よろしくお願い申し上げます'
    body12 = '喜和産業株式会社'
    body13 = '代表取締役社長'
    body14 = '安岡進一郎'
    outcnt = 0
    incnt = 0

    # Outlookアプリケーションをインスタンス化
    #outlook = win32com.client.Dispatch('Outlook.Application')

    #pythoncom.CoInitialize()

    for i in range(2,101):
        incnt += 1
        # 各内容のセット
        if ws.cell(row=i,column=13).value == 0:
            outcnt += 1
            com_mailto = ws.cell(row=i,column=14).value #宛先主メールアドレス
            #com_mailcc = ret_rows[i][15] #宛先Ccメールアドレス
            com_mailbcc = 'shinichiro@kiwasangyo.co.jp;yuuki@kiwasangyo.co.jp'
            #com_mailname1 = ret_rows[i][16] #宛先氏名1
            if ws.cell(row=i,column=6).value != None:
                com_mailname1 = ws.cell(row=i,column=6).value #社名
            else:
                com_mailname1 = ''

            if ws.cell(row=i,column=7).value != None:
                com_mailname2 = ws.cell(row=i,column=7).value #練習場名
            else:
                com_mailname2 = ''

            if ws.cell(row=i,column=5).value != None:
                com_mailname3 = ws.cell(row=i,column=5).value #役職
            else:
                com_mailname3 = ''
            
            com_mailname4 = ws.cell(row=i,column=4).value + '様' #氏名
            
            # Outlookアプリケーションをインスタンス化
            #pythoncom.CoInitialize()
            try:
                outlook = win32com.client.Dispatch('Outlook.Application')
                #mapi = outlook.GetNamespace("MAPI")
                #draft_folder = mapi.GetDefaultFolder(16) 
                # メールオブジェクトの作成　要素の設定
                #if incnt == 1:
                time.sleep(10)
                mail = outlook.CreateItem(0) # 0:メール
                time.sleep(5)
                mail.to = com_mailto
                mail.bcc = com_mailbcc
                mail.subject = subject_org 
                #mail.bodyFormat = 1 #テキスト形式

                mailbody1 = com_mailname1 + '\r\n' + com_mailname2  + '\r\n' + com_mailname3 + '\r\n' + com_mailname4 
                mailbody2 = '\r\n' + '\r\n' + body1 + '\r\n' + body2 + '\r\n' + body3 + '\r\n' + body4 + '\r\n' + body5 + '\r\n' + body6 + '\r\n' + body7 + '\r\n' + body8
                mailbody3 = '\r\n' + '\r\n' + body9 + '\r\n' + body10 + '\r\n' + body11
                mailbody4 = '\r\n' + '\r\n' + '\r\n' + '\r\n' + body12 + '\r\n' + body13 + '\r\n' + body14

                mail.body = mailbody1 +  mailbody2 + mailbody3 + mailbody4 

                #mail.save()
                #mail.Move(draft_folder)


                # 送信前に確認（Outlookが起動）
                mail.display(True)
                ws.cell(row=i,column=13).value = 1
                #mail.Send()
            except Exception as e:
                print(f"メール送信に失敗しました: {str(e)}  {str(com_mailname4)}")

            #pythoncom.CoUninitialize()
            # メール送信
            #mail.Send()
    wb.save            
    print('処理終了 : ',datetime.datetime.now())   
    print('出力件数 : ',outcnt)         