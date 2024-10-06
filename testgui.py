import tkinter as tk
import sys

class MainWindow:
    def __init__ (self, master):
        self.master = master
        self.master.title("Example Application")
        self.master.geometry("300x300")
        
        self.label = tk.Label (master, text ="Example")
        self.label.config(font=("", 15))
        self.label.pack(padx=20, pady=30, fill=tk.BOTH)
        
        self.input = tk.Entry(master, width=50)
        self.input.pack(padx=20, pady=30, fill=tk.BOTH)
        
        self.btnOK = tk.Button(master, text="OK", command=lambda: output(self.input.get()))
        self.btnOK.config(height=1, width=30)
        self.btnOK.pack(pady=10) 
        
        self.btnExit = tk.Button(master, text="Exit", command=lambda: on_exit(master))
        self.btnExit.config(height=1, width=30)
        self.btnExit.pack(pady=10)

def output(input):
    root = tk.Toplevel()
    OutputWindow(root, input)

class OutputWindow (object):
    def __init__(self, root, input):
        self.root = root
        self.root.geometry("300x200")
        self.input = input
        
        self.label = tk.Label (self.root, text =input + " is input")
        self.label.config(font=("", 15))
        self.label.pack(padx=20, pady=30, fill=tk.BOTH)
        
        self.btn = tk.Button(self.root, text="OK", command=lambda: self.root.destroy())
        self.btn.config(height=1, width=30)
        self.btn.pack(pady=10) 

def on_exit(root):
    root.destroy()
    sys.exit()
    return

if __name__ == '__main__':
    root = tk.Tk()
    main = MainWindow(root)
    root.mainloop()