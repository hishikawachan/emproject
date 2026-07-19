import smtplib
#from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os


# メールの設定
#msg = EmailMessage()
msg = MIMEMultipart()
#msg.set_content("PythonからGmail送信に成功しました！")

msg["Subject"] = "テストメール（ファイル添付テスト）"
msg["From"] = "hishikawachan@gmail.com"
msg["To"] = "hishikaw901014@gmail.com"

body = "このメールにはファイルが添付されています。ご確認ください。"
msg.attach(MIMEText(body, "plain"))

file_path = "sample.pdf"

#添付ファイルを読み込み
with open(file_path, "rb") as f:
    file = MIMEApplication(f.read(), _subtype="pdf")
    file.add_header("Content-Disposition", "attachment", filename=os.path.basename(file_path))
    msg.attach(file)

# Gmailに接続して送信
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login("ishikawa.kiwa@gmail.com", "njhqdgwqxrpcwlky")
    smtp.send_message(msg)



""" # SMTPサーバーへ接続して送信
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login("hishikawachan@gmail.com", "cjddvjeuwvuuquwc")
    smtp.send_message(msg) """