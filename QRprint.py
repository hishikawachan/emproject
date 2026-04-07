import win32com.client

# ===== 設定 =====
TEMPLATE_PATH = r"C:\My Labels\QRver.lbx"
PRINTER_NAME = "Brother PT-P950NW (1 コピー)"   # Windowsのプリンタ名
QR_TEXT = "KCD2:mt-001:KIW001:27"   # 印刷したいQRコード内容
PRINT_COPIES = 1

# ===== b-PAC COMオブジェクト生成 =====
bpac = win32com.client.Dispatch("bpac.Document")

# テンプレートを開く
if not bpac.Open(TEMPLATE_PATH):
    raise RuntimeError("テンプレートを開けませんでした")

try:
    # プリンタ指定（有線LANでも通常これでOK）
    #bpac.SetPrinter(PRINTER_NAME, True)

    # QRコードオブジェクトの内容を書き換え
    # b-PACでは QR も「Text」として扱う
    #bpac.GetObject("QR_DATA").Text = QR_TEXT
    # 印刷
    # プリンタ名のリストを取得
    """ printers = bpac.Printer.GetInstalledPrinters

    if not printers:
        print("利用可能なプリンタが見つかりません")
        exit
    else:
        # リストの最初のプリンタ名を選択
        selected_printer = printers[0]
        bpac.SetPrinter(selected_printer, True) """
    bpac.SetPrinter(PRINTER_NAME, True) 
    # QRコードオブジェクトの内容を書き換え
    # b-PACでは QR も「Text」として扱う
    bpac.GetObject("QR_DATA").Text = QR_TEXT
    bpac.StartPrint("", 0)
    bpac.PrintOut(PRINT_COPIES, 0)
    bpac.EndPrint()

finally:
    # ドキュメントを閉じる
    bpac.Close()

