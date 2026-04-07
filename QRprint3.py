import win32com.client
import json

# ==== 設定 ====
TEMPLATE_PATH = r"C:\My Labels\QRlabel.lbx"  # P-touch Editorで作成したテンプレート
PRINTER_NAME = "Brother PT-P950NW"

def load_from_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def print_ready():
    # b-PACオブジェクト作成
    bpac = win32com.client.Dispatch("bpac.Document")

    # テンプレートを開く
    if not bpac.Open(TEMPLATE_PATH):
        print("テンプレートが開けません")
        return

    # プリンター指定
    bpac.SetPrinter(PRINTER_NAME, False)

    return bpac

def print_qr(b_pac,QR_DATA,QR_TEXT):
    
    # QRオブジェクトにデータ設定（テンプレ内のオブジェクト名と一致させる）
    qr_obj1 = b_pac.GetObject("QR_CODE")
    qr_obj1.Text = QR_DATA
    #qr_obj2 = b_pac.GetObject("QR_DATA")
    #r_obj2.Text = QR_TEXT

    # 印刷実行
    b_pac.StartPrint("", 0)
    b_pac.PrintOut(1, 0)

    print("印刷完了")

if __name__ == "__main__":
    items = load_from_json("labels2.json")
    b_pac = print_ready()
    for item in items:
        qr = item["qr"]
        qrtext = item["part_no"]
        print_qr(b_pac,qr,qrtext)
