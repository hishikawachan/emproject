import yaml
import sys
from tkinter import messagebox
from calendar import day_abbr
import datetime
from datetime import datetime

class Publiclib:
    def __init__(self):
        pass

    # 共通yaml情報取得
    def load_yaml(self):
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
            parm.append(config['rep_title']) 
            parm.append(config['rep_geometry'])   
            parm.append(config['report_title']) 
            parm.append(config['report_geometry'])   
            parm.append(config['culcinput_title']) 
            parm.append(config['culcinput_geometry'])                
        return parm
    
    # 共通日付(8桁)チェック
    def date_check(self, start_date, end_date):
        # 入力値　数値チェック
        try:
            int(start_date, 10)
        except ValueError:
            return 6
        try:
            int(end_date, 10)
        except ValueError:
            return 7
        # 入力値 日付比較チェック
        if int(end_date, 10) - int(start_date, 10) < 0:
            return 8
        # 入力値 日付存在チェック
        s_year = int(start_date[:4])
        s_month = int(start_date[4:6])
        s_day = int(start_date[6:])
        e_year = int(end_date[:4])
        e_month = int(end_date[4:6])
        e_day = int(end_date[6:])
        try:
            s_newDataStr="%04d/%02d/%02d"%(s_year,s_month,s_day)
            s_newDate=datetime.strptime(s_newDataStr,"%Y/%m/%d")
            e_newDataStr="%04d/%02d/%02d"%(e_year,e_month,e_day)
            e_newDate=datetime.strptime(e_newDataStr,"%Y/%m/%d")
            return 0
        except ValueError:
            return 9
    # 共通日付(8桁)変換
    def date_conv(self, start_date, end_date):
        str_start = start_date + '000000'
        str_end = end_date + '235959'
        date_list = []
        date_list.append(datetime.strptime(str_start, '%Y%m%d%H%M%S'))
        date_list.append(datetime.strptime(str_end, '%Y%m%d%H%M%S'))
        return date_list

    # メッセージボックス出力
    def messagebox_output(self, msg): 
        messagebox.showinfo(msg)

    # 終了ボタン処理
    def on_exit(self,root):
        root.destroy()
        sys.exit()
        return
    
    # 戻るボタン処理
    def on_return(self,root):
        root.destroy()
        #sys.exit()
        return
    
    # ディストラクタ
    def __del__(self):        
        pass     