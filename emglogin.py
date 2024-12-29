import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
from emgpublib import Publiclib
from emgmenu import Menuproc

# ログイン処理
class Loginproc:
    def __init__(self, master, parms):
        self.root_0 = master
        self.parms = parms
        # 初期処理
        # ログイン画面の設定
        self.root_0.title(self.parms[0]) 
        self.root_0.geometry(self.parms[1]) 
        self.root_0.resizable(0, 0)

        # ウィジェットの配置や、イベント処理などを記述
        # ユーザーID
        self.label_1 = tk.Label(self.root_0, text="ユーザーID")
        self.label_1.place(x=20, y=20)
        self.entry_1 = tk.Entry(self.root_0, width=15, font=("Arial", 10))
        self.entry_1.place(x=100, y=20)

        # パスワード
        self.label_2 = tk.Label(self.root_0, text="パスワード")
        self.label_2.place(x=20, y=50)
        self.entry_2 = tk.Entry(self.root_0, width=15, font=("Arial", 10))
        self.entry_2.place(x=100, y=50)

        # ログインボタン
        self.button_1 = tk.Button(self.root_0, text="ログイン", command=lambda: self.on_check(self.entry_1.get(), self.entry_2.get()))
        self.button_1.place(x=180, y=80)

        # 終了ボタン
        self.button_2 = tk.Button(self.root_0, text="終了", command=lambda: self.close(self.root_0))
        self.button_2.place(x=230, y=80)

        # メッセージ領域
        self.label_2 = tk.Label(self.root_0, text="")
        self.label_2.place(x=230, y=120)
    
    # ログイン処理
    def on_check(self, entry_1, entry_2):
        if entry_1 != "":
            if entry_2 != "":
                ret = self.login_proc(entry_1, entry_2)
                if ret:
                    self.label_2['text'] = "ユーザーID又はパスワードが間違っています"
                else:
                    self.label_2['text'] = ""
                    #res = main_out() 
                    root_1 = tk.Toplevel()
                    remenu = Menuproc(root_1, self.parms)
    
    # ログインチェック
    def login_proc(self, id, password):
        if self.parms[2] == id:
            if self.parms[3] == password:
                return 0
            else:
                return 9
        return 9
    
    # 終了処理
    def close(self, root):
        repub = Publiclib()
        ret = repub.on_exit(root)

