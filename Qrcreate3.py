import zipfile
import os

# 対象フォルダー（例：同じ階層の xml_folder）
target_folder = r"C:\My Labels"

# 出力するZIPファイル名
zip_name = r"c:\My labels\qrcode.zip"

with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(target_folder):
        for file in files:
            if file.lower().endswith(".xml"):
                full_path = os.path.join(root, file)
                # ZIP内のパス（フォルダー構造を保持）
                arcname = os.path.relpath(full_path, target_folder)
                zipf.write(full_path, arcname)

print("XMLファイルの圧縮が完了しました！")
