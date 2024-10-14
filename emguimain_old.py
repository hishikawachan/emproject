# ライブラリのインポート
import tkinter as tk
from tkinter import ttk
import yaml
import tkinter.filedialog as filedialog
from tkinter import messagebox
import time
import sys 


# ログイン
class Guilogin:
    def __init__(self, master=None):
        self.master = master
        # 初期処理
        # yamlファイルから共通データ取得
        re_parm = load_yaml()
        # ログイン画面の設定
        self.master.title(re_parm[0]) 
        self.master.geometry(re_parm[1]) 
        self.master.resizable(0, 0)

        # ウィジェットの配置や、イベント処理などを記述
        # ユーザーID
        self.label_1 = tk.Label(master, text="ユーザーID")
        self.label_1.place(x=20, y=20)
        self.entry_1 = tk.Entry(master, width=15, font=("Arial", 10))
        self.entry_1.place(x=100, y=20)

        # パスワード
        self.label_2 = tk.Label(master, text="パスワード")
        self.label_2.place(x=20, y=50)
        self.entry_2 = tk.Entry(master, width=15, font=("Arial", 10))
        self.entry_2.place(x=100, y=50)

        # ログインボタン
        self.button_1 = tk.Button(master, text="ログイン", command=lambda: self.on_check(self.entry_1.get(), self.entry_2.get()))
        self.button_1.place(x=180, y=80)

        # 終了ボタン
        self.button_2 = tk.Button(master, text="終了", command=lambda: on_exit(master))
        self.button_2.place(x=230, y=80)

        # メッセージ領域
        self.label_2 = tk.Label(master, text="")
        self.label_2.place(x=230, y=120)
    
    # ログイン処理
    def on_check(self, entry_1, entry_2):
        if entry_1 != "":
            if entry_2 != "":
                ret = self.login_proc(entry_1, entry_2)
                if ret:
                    #messagebox_output("ユーザーID又はパスワードが間違っています")  
                    self.label_2['text'] = "ユーザーID又はパスワードが間違っています"
                else:
                    self.label_2['text'] = ""
                    #res = main_out() 
                    root_1 = tk.Toplevel()
                    Mainmenu(root_1)
    
    # ログインチェック
    def login_proc(self, id, password):
        re_parm = load_yaml()
        if re_parm[2] == id:
            if re_parm[3] == password:
                return 0
            else:
                return 9
        return 9
    
# def output(input):
#     root = tk.Toplevel()
#     OutputWindow(root, input)

# class OutputWindow (object):
#     def __init__(self, root, input):
#         self.root = root
#         self.root.geometry("300x200")
#         self.input = input
        
        # self.label = tk.Label (self.root, text =input + " is input")
        # self.label.config(font=("", 15))
        # self.label.pack(padx=20, pady=30, fill=tk.BOTH)
        
        # self.btn = tk.Button(self.root, text="OK", command=lambda: self.root.destroy())
        # self.btn.config(height=1, width=30)
        # self.btn.pack(pady=10)

def load_yaml():
    parm = []
    # web操作用yamlファイルから共通データ取得
    with open('C:/em/emproject/emoneygui.yaml','r+',encoding="utf-8") as ry:
        config = yaml.safe_load(ry)
        parm.append(config['login_title']) 
        parm.append(config['login_geometry']) 
        parm.append(config['user_id'])
        parm.append(config['user_pass'])
        parm.append(config['menu_title']) 
        parm.append(config['menu_geometry']) 
    
    return parm

# メインメニュー表示・選択
class Mainmenu(object):
    def __init__(self, root_1):
        self.root_1 = root_1
         # yamlファイルから共通データ取得
        re_parm = load_yaml()
        # メインメニュー画面の設定
        self.root_1.title(re_parm[4]) 
        self.root_1.geometry(re_parm[5]) 
        self.root_1.resizable(0, 0)
        self.id = re_parm[2]
        self.password = re_parm[3]

        self.var: tk.StringVar = tk.StringVar()
        self.var.set("")

        # ラジオボタンの状態を管理するための変数を作成
        #var = tk.StringVar(value="期間設定売上管理レポート出力")  # 初期値を設定
        var = tk.StringVar(value="1b1")  # 初期値を設定

        #self.label_11 = tk.Label(self.root_1, text="実行する項目を選択し「決定」をクリックしてください")
        #self.label_11.place(x=200, y=30)

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

        # 終了ボタン
        self.button_12 = tk.Button(root_1, text="終了", command=lambda: on_exit(root_1))
        self.button_12.place(x=320, y=160)

        self.label_12 = tk.Label(root_1, text="実行する項目を選択し「決定」をクリックしてください")
        self.label_12.place(x=250, y=200)        
    
    # 選択されたボタン番号別処理へ分岐
    def proc_selection(self,event=None):
        self.selection = self.var.get()
        #self.label_12['text'] = self.selection
        if self.selection == '1b1':
            root_11 = tk.Toplevel()
            Report(root_11)
        if self.selection == '1b2':
            root_12 = tk.Toplevel()
            Gross(root_12)
        if self.selection == '1b3':
            root_13 = tk.Toplevel()
            Datashow(root_13)
        if self.selection == '1b4':
            root_14 = tk.Toplevel()
            Dataget(root_14)

# レポート出力画面表示
class Report(object):
    def __init__(self, root_11):
        self.root_11 = root_11
        pass

# 売上合計値出力画面表示
class Gross(object):
    def __init__(self, root_12):
        self.root_12 = root_12
        pass

# 取引履歴表示
class Datashow(object):
    def __init__(self, root_13):
        self.root_13 = root_13
        pass

# データ取込み画面表示
class Dataget(object):
    def __init__(self, root_14):
        self.root_14 = root_14
        pass


# 終了ボタン処理
def on_exit(root):
    root.destroy()
    sys.exit()
    return

# メッセージボックス出力
def messagebox_output(msg): 
    messagebox.showinfo(msg)                
 
if __name__ == "__main__":
    # メインループの実行
    root = tk.Tk()
    main = Guilogin(root)
    root.mainloop()
