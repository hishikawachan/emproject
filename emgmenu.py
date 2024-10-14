# ライブラリのインポート
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog

from emgpublib import Publiclib
from emgrepinput import Reportinput
from emgculcinput import Dataculcinput
from emgdatashowinput import Datashowinput
from emgdatagetinput import Datagetinput  


# メインメニュー表示・選択
class Menuproc(object):
    def __init__(self, root_1):
        self.root_1 = root_1
        # メインメニュー画面の設定
        # yamlファイルから共通データ取得
        repub = Publiclib()
        parms = repub.load_yaml()
        self.root_1.title(parms[4]) 
        self.root_1.geometry(parms[5]) 
        self.root_1.resizable(0, 0)
        self.id = parms[4]
        self.password = parms[5]

        del repub

        self.var: tk.StringVar = tk.StringVar()
        self.var.set("")

        # ラジオボタンの状態を管理するための変数を作成
        var = tk.StringVar(value="1b1")  # 初期値を設定

        # ラジオボタンを作成
        self.radiobutton1 = tk.Radiobutton(root_1, text="期間別売上管理レポート出力", variable=self.var, value="1b1")
        self.radiobutton2 = tk.Radiobutton(root_1, text="期間別売上合計値照会", variable=self.var, value="1b2")
        self.radiobutton3 = tk.Radiobutton(root_1, text="端末別決済履歴照会", variable=self.var, value="1b3")
        self.radiobutton4 = tk.Radiobutton(root_1, text="売上情報取込み(期間設定)", variable=self.var, value="1b4")

        # ラジオボタンをウィンドウに配置
        self.radiobutton1.place(x=200, y=60)
        self.radiobutton2.place(x=200, y=80)
        self.radiobutton3.place(x=200, y=100)
        self.radiobutton4.place(x=200, y=120)

        # 決定ボタン
        self.button_11 = tk.Button(root_1, text="決定", command=self.proc_selection) 
        self.button_11.place(x=250, y=160)

        # 戻るボタン
        self.button_12 = tk.Button(root_1, text="戻る", command=lambda: self.close(root_1))
        self.button_12.place(x=320, y=160)

        self.label_12 = tk.Label(root_1, text="実行する項目を選択し「決定」をクリックしてください")
        self.label_12.place(x=250, y=200)        
    
    # 選択されたボタン番号別処理へ分岐
    def proc_selection(self,event=None):
        self.selection = self.var.get()
        #self.label_12['text'] = self.selection
        if self.selection == '1b1':
            root_11 = tk.Toplevel()
            rerep = Reportinput(root_11)
        if self.selection == '1b2':
            root_12 = tk.Toplevel()
            recul = Dataculcinput(root_12)
        if self.selection == '1b3':
            root_13 = tk.Toplevel()
            repshw = Datashowinput(root_13)
        if self.selection == '1b4':
            root_14 = tk.Toplevel()
            reget = Datagetinput (root_14)
    
    # 終了処理
    def close(self, root):
        repub = Publiclib()
        ret = repub.on_return(root)

