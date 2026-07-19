import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
from datetime import datetime as dt
import time

from emgpublib import Publiclib
from emgculc import Culccontrol

# 売上合計値出力画面表示
class Dataculcinput(object):
    def __init__(self, root_12, parms):
        self.root_12 = root_12
        self.parms = parms
        # レポート出力の設定
        # yamlファイルから共通データ取得
        self.root_12.title(self.parms[10]) 
        self.root_12.geometry(self.parms[11]) 
        self.root_12.resizable(0, 0)
        self.id = self.parms[2]
        self.password = self.parms[3]
        
        # ウィジェットの配置や、イベント処理などを記述
        # 対象開始日
        self.label_121 = tk.Label(self.root_12, text="対象日付(FROM: yyyymmdd)")
        self.label_121.place(x=20, y=20)
        self.entry_121 = tk.Entry(self.root_12, width=15, font=("Arial", 10))
        self.entry_121.place(x=180, y=20)

        # 対象終了日
        self.label_122 = tk.Label(self.root_12, text="対象日付(TO: yyyymmdd)")
        self.label_122.place(x=20, y=50)
        self.entry_122 = tk.Entry(self.root_12, width=15, font=("Arial", 10))
        self.entry_122.place(x=180, y=50)

        # 実行ボタン
        self.button_121 = tk.Button(self.root_12, text="実行", command=lambda: self.date_check(self.entry_121.get(), self.entry_122.get()))
        self.button_121.place(x=180, y=80)

        # 戻るボタン
        self.button_122 = tk.Button(self.root_12, text="戻る", command=lambda: self.close(self.root_12))
        self.button_122.place(x=230, y=80)

        # メッセージ領域y
        self.label_123 = tk.Label(self.root_12, text="売上集計期間を指定してください(From <= To)")
        self.label_123.place(x=230, y=120)

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
                    root_121 = tk.Toplevel()
                    recul = Culccontrol(root_121, self.id, dates[0], dates[1]) 
                    reout = recul.culc_proc()
                    #reout = recul.report_output()
                    if reout:
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