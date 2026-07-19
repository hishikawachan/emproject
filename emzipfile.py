# -*- coding: utf-8 -*-
# ======================================
# 
# 電子マネー管理システム
# ファイル圧縮制御classモジュール
# 
#
# [環境]
#   Python 3.10.8
#   VSCode 1.64
#   <拡張>
#     |- Python  V2021.12
#     |- Pylance V2021.12
#
# [更新履歴]
#   2023/3/16  新規作成
#   2023/11/4  新バージョン作成
# ======================================
import os
import zipfile
import glob

class Zipfilecreate:
    def __init__(self,dir_main, compaycd, dir_date):  
        
        zip_name = dir_date + '.zip'
        self.findfile_name = os.path.join(dir_main, compaycd, '*.zip') 
        self.zipfile_name = os.path.join(dir_main, compaycd, zip_name) 
        self.dir_files_file = os.path.join(dir_main, compaycd, dir_date)
        self.dir_main = dir_main
        self.comcode = compaycd
        self.dir_date = dir_date
    
    def filezip(self):
        files_file = [
        f for f in os.listdir(self.dir_files_file) if os.path.isfile(os.path.join(self.dir_files_file, f))
        ]  

        # 書き出すzipファイルがあったら削除
        find_file = glob.glob(self.findfile_name)
        if len(find_file) > 0:
            for i in range(0,len(find_file)):
                os.remove(find_file[i])

        files_no = len(files_file)
        with zipfile.ZipFile(self.zipfile_name, 'w',
                        compression=zipfile.ZIP_DEFLATED,
                        compresslevel=6) as zf:
            for i in range(0,files_no):
                add_file = os.path.join(self.dir_main, self.comcode, self.dir_date, str(files_file[i])) 
                zf.write(add_file, arcname=str(files_file[i]))
        return i

    