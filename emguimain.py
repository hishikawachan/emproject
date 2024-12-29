# ライブラリのインポート
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog

from emglogin import Loginproc
from emgpublib import Publiclib


    
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
       
 
if __name__ == "__main__":
    # メインループの実行
    repub = Publiclib()
    parms = repub.load_yaml()
    root = tk.Tk()
    reg = Loginproc(root, parms)
    root.mainloop()
