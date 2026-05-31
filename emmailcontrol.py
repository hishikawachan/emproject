# -*- coding: utf-8 -*-
# ======================================
# 
# 電子マネー管理システム
# メール送信制御メインモジュール
# 処理対象の会社に指定帳票を添付してメールを送る
# 
# [環境]
#   Python 3.10.8
#   VSCode 1.64
#   <拡張>
#     |- Python  V2021.12
#     |- Pylance V2021.12
#
# [更新履歴]
#   2024/6/16  新規作成
#   
# ======================================
from datetime import datetime
import datetime
import yaml
import os
import win32com.client
from emdbclass import DataBaseClass

#====以下Gmail版用ライブラリ======================
import smtplib
#from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
#################################################################
# 共通パラメータ
#################################################################
parm_data = []

#################################################################
# メイン
#################################################################
if __name__ == "__main__":    

    print('処理開始：',datetime.datetime.now()) 
    
    # 基本情報取得
                
    #データベース操作クラス初期化及び共通パラメータyamlファイルから取得
    resdb = DataBaseClass('0') 
    
    #会社データ全件取得
    ret_rows = resdb.company_data_allget()

    # mail操作用yamlファイルから共通データ取得
    with open(r'C:\Users\hishi\OneDrive\Labo\em\emproject\yaml\emoneymail.yaml','r+',encoding="utf-8") as rm:
            config_yaml = yaml.safe_load(rm)
            subject_org = config_yaml['head']
            body1 = config_yaml['body1']
            body2 = config_yaml['body2']
            body3 = config_yaml['body3']
            body4 = config_yaml['body4']
            body5 = config_yaml['body5']
            foot1 = config_yaml['foot1']
            foot2 = config_yaml['foot2']
    # mail添付ファイルフォルダ
    with open('c:/em/emproject/emoney.yaml','r+',encoding="utf-8") as ry:
            config_yaml = yaml.safe_load(ry)
            file_path = config_yaml['dir_filepath']                   
    ########################################
    #
    # 会社データ毎の処理
    # 会社DBをシーケンスに読み、処理対象の会社を検知したらDB書込み及び帳票出力を行う
    # 会社データ　処理予定日 <= 処理日
    #
    ########################################        
    for i in range(0,len(ret_rows)):
        # 今日の日付と登録された処理予定日の比較
        t_date =  ret_rows[i][4]
        d = datetime.datetime.today()
        today = d.date()        
        td = today - t_date
        # 処理予定日<=今日なら処理対象とする
        if td.days >= 0:            
            print('*****************************************')
            print('対象会社 :',ret_rows[i][1])
            #debug
            print('対象会社へメール作成 :',datetime.datetime.now())
        
            parm_data = []
            data_cnt = 0
            #共通パラメータセット
            start_date = ret_rows[i][7]  #更新開始日セット
            end_date   = ret_rows[i][8]  #更新終了日セット
            com_code = ret_rows[i][0]    #対象会社コード
            com_mailto = ret_rows[i][14] #宛先主メールアドレス
            com_mailcc = ret_rows[i][15] #宛先Ccメールアドレス
            com_mailname1 = ret_rows[i][16] #宛先氏名1
            if ret_rows[i][17] != None:
                com_mailname2 = ret_rows[i][17] #宛先氏名2
            else:
                com_mailname2 = ''
            if ret_rows[i][18] != None:
                com_mailname3 = ret_rows[i][18] #宛先氏名3
            else:
                com_mailname3 = '' 
            # Outlookアプリケーションをインスタンス化
            outlook = win32com.client.Dispatch('Outlook.Application')
            # メールオブジェクトの作成要素の設定
            mail = outlook.CreateItem(0) # 0:メール
            mail.to = com_mailto
            if com_mailcc != None:
                mail.cc = com_mailcc
            mail.subject = subject_org + '   ' + str(start_date) + '～' + str(end_date) 
            mail.bodyFormat = 1 #テキスト形式

            mailbody1 = com_mailname1 + '\r\n' + com_mailname2 + '\r\n' + com_mailname3 + '\r\n'
            mailbody2 = body1 + '\r\n' + body2 + '\r\n' + body3 + '\r\n' + body4 +  '\r\n' + body5 + '\r\n'
            mail.body = mailbody1 + '\r\n' + mailbody2 + '\r\n' + '\r\n' + foot1 + '\r\n' + foot2
            
            # 添付ファイル抽出
            attach_dir = os.path.join(file_path, com_code)
            SYEAR = start_date.year
            SMONTH = start_date.month
            SDAY = start_date.day
            EYEAR = end_date.year
            EMONTH = end_date.month
            EDAY = end_date.day
            dir_date = str(com_code) + '_'+str(SYEAR)+str(SMONTH)+str(SDAY)+'_'+str(EYEAR)+str(EMONTH)+str(EDAY)+'.zip'
            attch_file = os.path.join(attach_dir, dir_date) 
            mail.Attachments.Add(attch_file)

            """ #添付ファイルを読み込み
            with open(attch_file, "rb") as f:
                file = MIMEApplication(f.read(), _subtype="zip")
                file.add_header("Content-Disposition", "attachment", filename=os.path.basename(attch_file))
                mail.attach(file) """

            # メールを保存
            # mail.Save()
            #mail.Move(draft_folder)

            # 送信前に確認（Outlookが起動）
            mail.display(True)
            # メール送信
            #mail.Send()

            """ #メールアドレス使用不可に対する暫定措置（gmail使用版）
            # メールの設定
            msg = MIMEMultipart()
            mail_subject = subject_org + '   ' + str(start_date) + '～' + str(end_date) 
            msg["Subject"] = mail_subject
            msg["From"] = "ishikawa.kiwa@gmail.com"
            msg["To"] = ",".join(com_mailto)
            if com_mailcc != None:
                msg['Cc'] = ",".join(com_mailcc)

            mailbody1 = com_mailname1 + '\r\n' + com_mailname2 + '\r\n' + com_mailname3 + '\r\n'
            mailbody2 = body1 + '\r\n' + body2 + '\r\n' + body3 + '\r\n' + body4 +  '\r\n' + body5 + '\r\n'
            mail_body = mailbody1 + '\r\n' + mailbody2 + '\r\n' + '\r\n' + foot1 + '\r\n' + foot2
            msg.attach(MIMEText(mail_body, "plain"))

            # 添付ファイル抽出
            attach_dir = os.path.join(file_path, com_code)
            SYEAR = start_date.year
            SMONTH = start_date.month
            SDAY = start_date.day
            EYEAR = end_date.year
            EMONTH = end_date.month
            EDAY = end_date.day
            dir_date = str(com_code) + '_'+str(SYEAR)+str(SMONTH)+str(SDAY)+'_'+str(EYEAR)+str(EMONTH)+str(EDAY)+'.zip'
            attch_file = os.path.join(attach_dir, dir_date) 
            
            #添付ファイル読み込み
            with open(attch_file, "rb") as attachment:
                part = MIMEBase("application", "zip")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{attch_file}"')
                msg.attach(part)

            # Gmailに接続して送信
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login("ishikawa.kiwa@gmail.com", "njhqdgwqxrpcwlky")
                smtp.send_message(msg) """
                
            #対象会社データ更新日の更新
            input_update = input('次回処理日をセットしますか(y or n):') 
    
            if input_update == 'y':
                res_row = resdb.company_updateday_update(com_code)
                
            os.remove(attch_file)                 
    
    del resdb
    print('処理終了：',datetime.datetime.now())            