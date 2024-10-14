import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
from datetime import datetime as dt
import time

from emgpublib import Publiclib
from emgreport import Reportcontrol

# レポート出力画面表示
class Reportinput(object):
    def __init__(self, root_11):
        self.root_11 = root_11
       
        # レポート出力の設定
         # yamlファイルから共通データ取得
        repub = Publiclib()
        parms = repub.load_yaml()
        self.root_11.title(parms[6]) 
        self.root_11.geometry(parms[7]) 
        self.root_11.resizable(0, 0)
        self.id = parms[2]
        self.password = parms[3]
        
        # ウィジェットの配置や、イベント処理などを記述
        # 対象開始日
        self.label_11 = tk.Label(self.root_11, text="対象日付(FROM)")
        self.label_11.place(x=20, y=20)
        self.entry_11 = tk.Entry(self.root_11, width=15, font=("Arial", 10))
        self.entry_11.place(x=100, y=20)

        # 対象終了日
        self.label_12 = tk.Label(self.root_11, text="対象日付(TO)")
        self.label_12.place(x=20, y=50)
        self.entry_12 = tk.Entry(self.root_11, width=15, font=("Arial", 10))
        self.entry_12.place(x=100, y=50)

        # 実行ボタン
        self.button_11 = tk.Button(self.root_11, text="実行", command=lambda: self.date_check(self.entry_11.get(), self.entry_12.get()))
        self.button_11.place(x=180, y=80)

        # 戻るボタン
        self.button_12 = tk.Button(self.root_11, text="戻る", command=lambda: self.close(self.root_11))
        self.button_12.place(x=230, y=80)

        # メッセージ領域
        self.label_12 = tk.Label(self.root_11, text="")
        self.label_12.place(x=230, y=120)
    
    # 処理入力日付チェック及び出力実行
    def date_check(self, start_date, end_date):
        if start_date != "":
            if end_date != "":
                ret = self.date_check_proc(start_date, end_date)
                if ret:
                    self.label_12['text'] = "対象日付が間違っています"
                else:
                    repub = Publiclib()
                    dates = repub.date_conv(start_date, end_date)
                    del repub
                    self.label_12['text'] = "指定されたレポートを出力中です"
                    time.sleep(2)
                    reprt = Reportcontrol(self.id, dates[0], dates[1]) 
                    if reprt:
                        self.label_12['text'] = "レポート出力に失敗しました"
                        time.sleep(3)
                        self.close(self.root_11)
                    else:
                        self.label_12['text'] = "レポート出力が終了しました"
                        time.sleep(3)
                        self.close(self.root_11)
    #日付論理チェック
    def date_check_proc(self, start_date, end_date):
        repub = Publiclib()
        redt = repub.date_check(start_date, end_date)
        del repub
        return redt

    # 終了処理
    def close(self, root):
        repub = Publiclib()
        ret = repub.on_return(root)