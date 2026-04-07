import win32com.client

LABEL_FILE = r"C:\My Labels\QRver.lbx"
QR_DATA = "http://schemas.brother.info/ptouch/2007/lbx/main" 
TEXT_DATA = "KCD2:mt-001:KIW001:27",

bpac = win32com.client.Dispatch("bpac.Document")

# テンプレを開く
if not bpac.Open(LABEL_FILE):
    raise RuntimeError("ラベルテンプレを開けません")

# QRコードにデータを設定
#bpac.GetObject("QRCode").Text = QR_DATA
bpac.GetObject("QRCode").Text = TEXT_DATA

# テキスト（任意）
bpac.GetObject("LabelText").Text = TEXT_DATA

# 印刷開始
bpac.StartPrint("", 0)

# 1枚印刷（2にすると2枚）
bpac.PrintOut(1, 0)

bpac.EndPrint()
bpac.Close()

print("印刷完了")
