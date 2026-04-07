
# 必要なライブラリをインポート
import xml.etree.ElementTree as ET
import os
import zipfile
import shutil
import win32com.client
import pythoncom
from pathlib import Path
import glob
import time 

#第1引数ファイル名の拡張子を第2引数に変更して返す
def change_extension(filename, new_extension):
    base_name = os.path.splitext(filename)[0]
    new_filename = base_name + new_extension
    return new_filename


print("ピータッチ印刷テスト開始")
#ベースとなる印刷データlbxを複製する
shutil.copyfile(r"C:\My Labels\QRver.lbx", r"C:\My Labels\QRVer1.lbx")

# 変更したいファイルのパスと新しい拡張子を指定
old_file_path = r"C:\My Labels\QRVer1.lbx"
new_extension = ".zip"
# 新しい拡張子を持つファイル名を生成
new_file_path = change_extension(old_file_path, new_extension)
# あたらしいやつが存在したら　消す
if os.path.exists(new_file_path):
    os.remove(new_file_path)

# ファイルをリネームして保存
os.rename(old_file_path, new_file_path)

#zipフォルダを解凍 label.xml prop.xml を得る
with zipfile.ZipFile(new_file_path) as existing_zip:
    existing_zip.extractall(r"C:\My Labels")
#time.sleep(10)

# 名前空間を定義
namespaces = {
    "pt": "http://schemas.brother.info/ptouch/2007/lbx/main" 
}

#埋め込むコードリスト
"""
qrdata = [
"KCD2:mt-001:KIW001:27",
"KCD2:mt-001:KIW002:47",
"KCD2:mt-001:KIW003:67",
"KCD2:mt-001:KIW004:87",
"KCD2:mt-001:KIW005:10",
"KCD2:mt-001:KIW006:30",
"KCD2:mt-001:KIW007:50",
"KCD2:mt-001:KIW008:70",
"KCD2:mt-001:KIW009:90",
"KCD2:mt-001:KIW010:68" ] 
"""

qrdata = [
"KCD2:mt-001:KIW001:27",
"KCD2:mt-001:KIW002:47",
"KCD2:mt-001:KIW003:67"
                        ] 

for data in qrdata:
    # XMLファイルを読み込む
    file_path = r"C:\My Labels\label.xml"
    tree = ET.parse(file_path)
    root = tree.getroot()
    #対象タグを検索してデータ入替え
    for elem in root.findall(".//pt:data", namespaces):
        elem.text = data
        # 保存
        tree.write(file_path,encoding="utf-8",xml_declaration=True)
        print("指定した文字列を置換しました", data)

    # 既存のZIPファイル存在する場合消去
    if os.path.exists(r"C:\My Labels\qrcode.zip"):
        os.remove(r"C:\My Labels\qrcode.zip")
    #label.xmlを圧縮する
    # 対象フォルダー（例：同じ階層の xml_folder）
    target_folder = r"C:\My Labels"

    # 出力するZIPファイル名
    zip_name = r"C:\My Labels\qrcode.zip"

    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(target_folder):
            for file in files:
                if file.lower().endswith(".xml"):
                    full_path = os.path.join(root, file)
                    # ZIP内のパス（フォルダー構造を保持）
                    arcname = os.path.relpath(full_path, target_folder)
                    zipf.write(full_path, arcname)

    # 変更したいファイルのパスと新しい拡張子を指定
    comp_file_path = r"C:\My Labels\qrcode.zip"
    new_extension = ".lbx"
    # 新しい拡張子を持つファイル名を生成
    new_file_path = change_extension(comp_file_path, new_extension)
    # あたらしいやつが存在したら　消す
    if os.path.exists(new_file_path):
        os.remove(new_file_path)
    # ファイルをリネームして保存
    os.rename(comp_file_path, new_file_path)
    #shutil.copyfile(new_file_path, r"C:\Users\hishi\OneDrive\ドキュメント\My Labels\qrcode.lbx")

    #印刷セクション
    pythoncom.CoInitialize()
    bpac = win32com.client.DispatchEx("bpac.Document")
    # プリンタ名のリストを取得
    printers = bpac.Printer.GetInstalledPrinters

    if not printers:
        print("利用可能なプリンタが見つかりません")
        exit
    else:
        # リストの最初のプリンタ名を選択
        selected_printer = printers[0]
        bpac.SetPrinter(selected_printer, True)
        # プリンター指定(固定する)
        #oc.SetPrinter("Brother PT-9700PC",True)
        #dir = os.path.abspath(os.path.dirname(__file__))
        #dir = r"C:\Users\hishi\OneDrive\Labo\em\emproject\src"
        #lbx_path = os.path.join(dir, "qrcode.lbx")
        #hasOpened = doc.Open(lbx_path)
        #bpac = win32com.client.Dispatch(r"C:\My Labels\qrcode.lbx")
        # テンプレを開く
        if not bpac.Open(r"C:\My Labels\qrcode.lbx"): 
            raise RuntimeError("テンプレートを開けません")

        #doc.StartPrint("", 0x04000000)
        #doc.PrintOut(1, 0x04000000)

        print("印刷開始")
        # 印刷開始
        bpac.StartPrint("", 0)

        # 1枚印刷（2にすると2枚）
        bpac.PrintOut(1, 0)

        print("印刷待機中")
        time.sleep(120)

        #bpac.EndPrint()
        #bpac.Close()
        print("印刷終了")

print("ピータッチ印刷テスト終了")