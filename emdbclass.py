# -*- coding: utf-8 -*-
# ======================================
# 
# 電子マネー管理システム
# MariaDB 操作class　
# [環境]
#   Python 3.10.8
#   VSCode 1.64
#   <拡張>
#     |- Python  V2021.12
#     |- Pylance V2021.12
#
# [更新履歴]
#   2023/3/16  新規作成
#   2023/9/16  試験的に機能追加(金種別・時間別等のデータをSQLにて取得)
#   2023/10/24 取引明細データ抽出速度向上改良
#   2023/11/13 金種ラベル　カラム追加
# ======================================
from datetime import datetime
import datetime
import calendar
import os
import yaml
import csv
import jpholiday
import subprocess
import pandas as pd
from emdbaccess import dbAccessor
#import emoneyweather as ew
import emweather as ew

class DataBaseClass:
    #####################################
    # 初期化
    #
    # パラメタ
    # [0]:dbip
    # [1]:dbname
    # [2]:dbport
    # [3]:dbuser
    # [4]:dbpassword
    # [5]:帳票ファイル出力先ディレクトリ
    #
    #####################################
    def __init__(self):
        # 基本情報取得
        #with open('C:/emoney/emoney.yaml','r+',encoding="utf-8") as ry:
        with open('C:/Users/user/OneDrive/Workplace/emoney/emoney.yaml','r+',encoding="utf-8") as ry:
            config_yaml = yaml.safe_load(ry)
            self.dbip = config_yaml['dbip']
            self.dbname = config_yaml['dbmarianame']
            self.dbport = config_yaml['dbport']        
            self.dbuser = config_yaml['dbuser']
            self.dbpw = config_yaml['dbpw']
            self.outpath = config_yaml['dir_filepath']
            
        # DB接続
        self.cur = dbAccessor(self.dbname,  self.dbport, self.dbip, self.dbuser, self.dbpw)
        # DBバックアップ  
        print('データベースバックアップ(処理前)開始')          
        res = self.database_backup('1')    
    #####################################
    # テーブル名一覧を取得
    #####################################
    def init_return(self):
        parm_list = []
        parm_list.append(self.outpath)
        
        return parm_list   
    #####################################
    # テーブル名一覧を取得
    #####################################
    def tabele_name_list_get(self):
        ret_list = self.cur.table_name_get()
        
        return ret_list    
    ####################################    
    #　実データ書き込み
    ####################################
    def data_insert(self,row):
        output_sql = """
            INSERT INTO tbpaylog
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                   %s, %s, %s, %s, %s, %s, %s, %s)
        """
        if len(row) == 0:
            return 0
        else:
            num = self.cur.excecuteInsertmany(output_sql,row) 
            
            return num    
    ####################################    
    #　実データ書き込み IGNORE仕様
    ####################################
    def data_insert2(self,row):
        output_sql = """
            INSERT IGNORE INTO tbpaylog
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                    %s, %s, %s, %s, %s, %s, %s, %s)
        """
        if len(row) == 0:
            return 0
        else:
            num = self.cur.excecuteInsertmany(output_sql,row) 
            
            return num    
    #####################################
    # ヤマトフィナンシャルデータからニューツルミ1階分のみ検出
    #####################################
    def data_choice(self,row):
        #
        # ニューツル1階分を判定する
        #
        if row[6] == "JE10720600222":#交通系
            return 4
        if row[6] == "H2000080":#楽天
            return 1
        if row[8] == "ＷＡＯＮ":
            if int(row[6]) == 5050130000240:#WAON
                return 3
        if row[8] == "ｎａｎａｃｏ":
            if int(row[7]) >= 10000: #nanaco
                return 2
            
        return 9
    ####################################    
    #　ソート、集計用日付、時間生成
    # ##################################
    def date_set(self,year,month,day,hour,minute,second):
    
        #日付（数字）
        res_date1 = year * 10000 + month * 100 + day
        #日付（ハイフン付き文字列）
        res_date2 = str(year) + "-" + str(month) + "-" + str(day)
        #日付（文字列）
        res_date3 = str(year)  + str(month) +  str(day)
        #時間（文字列）
        res_date4 = str(hour) + str(minute) + str(second)
        
        return res_date1,res_date2,res_date3,res_date4    
    #######################################
    # 曜日・祝日検索
    #######################################
    def week_set(self,year,month,day):
        #曜日番号検索
        dt = datetime.date(year,month,day)
        week = dt.weekday()
        #祝日判定
        res_horiday = jpholiday.is_holiday_name(datetime.date(year,month,day))
        if res_horiday != None:
            flg = 1                
        else:
            res_horiday = " "
            flg = 0
            
        return week,flg,res_horiday    
    #######################################
    #　設置場所資産番号から設置場所番号を検索
    #######################################
    def set_placecd(self,sisancd):
        q_sql = f"""
                    SELECT *
                    FROM  tbplace
                    WHERE placesisancode = '{sisancd}'
                """   
        ret_rows = self.cur.excecuteQuery(q_sql)
        
        return ret_rows    
    #######################################
    #　会社コードから設置場所番号を検索し配列で受け取る
    #######################################
    def get_placecd(self,cocode):
        q_sql = f"""
                    SELECT placecode
                    FROM  tbplace
                    WHERE placecocode = '{cocode}'
                """   
        ret_rows = self.cur.excecuteQuery(q_sql)
        #設置場所番号抽出
        row = []
        i = 0
        for i in ret_rows:
            row.append(str(i[0]))
            
        return row    
    #######################################
    # 明細種別名称から明細種別番号を検索
    #######################################
    def set_meisaisyubetu(self,syubetsuname):
        q_sql = f"""
                    SELECT *
                    FROM  tbcard
                    WHERE cardname = '{syubetsuname}'
            """                
        ret_rows = self.cur.excecuteQuery(q_sql)
        
        return ret_rows    
    ######################################
    #対象年月の最新気象データに更新            
    ######################################
    def weather_data_output(self,prec,block,year,month):
        data_list = ew.weather_list_get(prec,block,year,month) 
        # 既存データ削除
        sql = f"""
                DELETE 
                FROM tbweather
                WHERE   prec = {prec}
                AND     block = {block}
                AND     year = {year}
                AND     month = {month} 

        """ 
        num1 = self.cur.excecuteDelete(sql)
        
        output_sql = """
            INSERT INTO tbweather
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                
        """
        num2 = self.cur.excecuteInsertmany(output_sql,data_list) 

        return num2,num1
    ####################################
    # 気象情報取得    
    ###################################        
    def weather_get(self,year,month,day,prec,block):        
        # 気象データ読む
        sql = f"""  
                    SELECT *
                    FROM tbweather
                    WHERE year = {year}
                    AND   month = {month}
                    AND   day = {day}
                    AND   prec = {prec}
                    AND   block = {block}
            """
        ret_rows = self.cur.excecuteQuery(sql)
        
        return ret_rows    
    ####################################
    # 気象情報取得 期間を絞ったデータ取得    
    ###################################        
    def weather_get2(self):        
        # 気象データ読む
        sql = f"""  
                    SELECT *
                    FROM tbweather
            """
        ret_rows = self.cur.excecuteQuery(sql)
        
        return ret_rows    
    ####################################
    # 気象情報取得 日付範囲指定での抽出    
    ###################################        
    def weather_get3(self,sdate,edate,prec,block):        
        # 気象データ読む
        sql = f"""  
                    SELECT *
                    FROM tbweather
                    WHERE date BETWEEN '{sdate}' AND '{edate}'
                    AND   prec = {prec}
                    AND   block = {block}
            """
        ret_rows = self.cur.excecuteQuery(sql)
        
        return ret_rows    
    ####################################
    # 気象情報取得 データ修正    
    ###################################        
    def weather_update(self,update_date,day,year,month):      
    
        s_sql = f"""
                UPDATE tbweather 
                SET date = '{update_date}'                              
                WHERE day = {day}
                AND   year = {year}
                AND   month = {month}
                """            
        ret_rows = self.cur.excecuteUpdate(s_sql)     
    ###############################################################
    # 会社データから全データ取得
    ############################################################### 
    def company_data_allget(self):
        s_sql =  f"""  
                    SELECT *
                    FROM tbcompany                
                """
        ret_rows = self.cur.excecuteQuery(s_sql) 
        
        return ret_rows    
    ###############################################################
    # 会社データから指定レコード取得
    ############################################################### 
    def company_data_get(self,companyid):
        s_sql = f'SELECT * FROM tbcompany WHERE comcode={companyid}'
        ret_rows = self.cur.excecuteQuery(s_sql) 
        
        return ret_rows    
    ###############################################################
    # 対象会社のcsvファイル読込み及びDB出力　売上明細
    ############################################################### 
    def uriagemeisai_output(self, companyid, sdate, edate, f_name):
        # 入力ファイル名の取得
        file_name = f_name.strip()
        input_filepath = os.path.join(self.outpath,file_name)  
        
        start_date = sdate
        end_date = edate
        out_err = 0
        in_count = 0
        out_count = 0
        sum_price = 0
    
        with open(input_filepath, encoding = 'shift-jis') as f:
            reader = csv.reader(f)            
            for row in reader :
                #sum_price = 0
                data_list = []
                # 日付範囲の判定
                # 決済日時取得
                if in_count == 0:
                    in_count += 1
                else:                
                    date_time = row[18]
                    verify_date = datetime.date(int(date_time[0:4]), int(date_time[4:6]), int(date_time[6:8]))
                    if (verify_date >= start_date) and (verify_date <= end_date) and (row[8][0:7] ==  companyid):
                        #練習データを排除する
                        if int(row[14]) <= 10: #明細種別11以上は練習データ
                            data_list = []
                            date_time = row[18]
                            data_list.append(int(date_time[0:4]))#決済年
                            data_list.append(int(date_time[4:6]))#決済月
                            data_list.append(int(date_time[6:8]))#決済日
                            data_list.append(int(date_time[8:10]))#決済時
                            data_list.append(int(date_time[10:12]))#決済分
                            data_list.append(int(date_time[12:14]))#決済秒
                            
                            kyear = int(date_time[0:4])#決済年
                            kmonth = int(date_time[4:6])#決済月
                            kday = int(date_time[6:8])#決済日
                            khour = int(date_time[8:10])#決済時
                            kminute = int(date_time[10:12])#決済分
                            ksecond = int(date_time[12:14])#決済秒            
                            
                            data_list.append(int(date_time[14:16]))#決済番号
                            data_list.append(int(row[2])) #設置場所番号
                            #data_list.append(str(row[12])) #明細区分番号
                            if row[12] == '00':#景品データは現金に変更
                                data_list.append('1')
                            else:
                                if row[12] == '01':
                                    data_list.append('1')
                                else:
                                    if row[12] == '02':
                                        data_list.append('2')
                                    else:
                                        data_list.append('F')                            
                            #景品のデータは現金に切替
                            if row[12] == '00':
                                data_list.append(5)
                            else:                    
                                if row[12] == '01': #現金のデータは明細種別を"5"にセット    
                                    data_list.append(5)
                                else:    
                                    data_list.append(int(row[14])) #明細種別番号               
                                
                            #景品のデータは1000円に切替
                            if row[12] == '00':    
                                data_list.append(1000) #決済金額
                                set_price = '1000'
                                sum_price += 1000
                            else:
                                data_list.append(int(row[17])) #決済金額
                                sum_price += int(row[17])
                                set_price = str(row[17])
                                
                            #検索日付・時間セット
                            res_list = self.date_set(kyear,kmonth,kday,khour,kminute,ksecond)
                            data_list.append(res_list[0])#日付（整数）
                            #data_list.append(res_list[1])#日付（ハイフン付文字列）
                            data_list.append(res_list[2])#時間（文字列）
                            data_list.append(res_list[3])#時間（文字列） 
                            #曜日・祝日セット
                            res_list = self.week_set(kyear,kmonth,kday)
                            data_list.append(res_list[0])#曜日コード
                            data_list.append(res_list[1]) #祝日フラグ 祝日なら'1' それ以外は'0'  
                            data_list.append(res_list[2])#祝日名（空白有） 
                            # 金種ラベル追加
                            data_list.append(set_price)#金種ラベル        
                            
                            #debug 
                            #if in_count % 100 == 0: #100件処理毎に表示
                            #    print('データ入力件数',in_count)
                            in_count += 1
                            
                            #DBへの書き込み(1件ずつ書込む方式)
                            data_list2 = []
                            data_list2.append(data_list)                        
                            data_num = self.data_insert2(data_list2) 
                            if data_num != None:
                                out_count +=  data_num   
                            else:
                                out_err += 1 
                            #debug 
                            #if out_count % 100 == 0: #100件処理毎に表示
                            #    print('データ出力件数',out_count)
                                        
                        else:
                            out_err += 1
                    else:
                        out_err += 1        
                    
        db_updatedate = date_time[0:4] + '-' + date_time[4:6] + '-' + date_time[6:8]
                        
        # if out_err > 0:
        #         print('入力不可件数：',out_err)
                
        if in_count == 0 and out_err == 0:
            edit_status = 9
        else:
            edit_status = 0
            
        #Debug
        print('入力件数',in_count-1)
        print('出力件数',out_count)
        print('入力不可件数',out_err)
        print('合計金額',sum_price)      
       
        return edit_status,out_count,out_err,db_updatedate    
    ###############################################################
    # 対象会社のcsvファイル読込み　TOAMAS及びDB出力
    ############################################################### 
    def income_output(self,companyid, sdate, edate, f_name):
        # 入力ファイル名の取得
        file_name = f_name.strip()
        input_filepath = os.path.join(self.outpath,file_name)  
        
        start_date = sdate
        end_date = edate
        out_err = 0
        in_count = 0
        out_count = 0
        sum_price = 0        
    
        with open(input_filepath, encoding = 'UTF-8') as f:
            reader = csv.reader(f)
            for row in reader :
                if row[2] != '現金' and row[3] != '未了（不明）' and row[3] != '未了（未書込）' : #現段階では現金データは対象外とする。未了は対象外
                    # 日付範囲の判定
                    # 決済日時取得
                    if in_count == 0:
                        in_count += 1
                    else:
                        date_time = row[0]
                        verify_date = datetime.date(int(date_time[0:4]), int(date_time[5:7]), int(date_time[8:10]))
                        if (verify_date >= start_date) and (verify_date <= end_date) and (row[8][0:7] ==  companyid):
                            data_list = []                   
                            date_time = row[0]
                            #売上日を日付と時間に分け,更に'/'と':'で分けて数字にする
                            datetime_list = date_time.split()
                            datetime_date = datetime_list[0].split('-')
                            datetime_time = datetime_list[1].split(':')       
                                    
                            data_list.append(int(datetime_date[0]))#決済年
                            data_list.append(int(datetime_date[1]))#決済月
                            data_list.append(int(datetime_date[2]))#決済日
                            data_list.append(int(datetime_time[0]))#決済時
                            data_list.append(int(datetime_time[1]))#決済分
                            data_list.append(int(datetime_time[2]))#決済秒
                            
                            kyear = int(datetime_date[0])#決済年
                            kmonth = int(datetime_date[1])#決済月
                            kday = int(datetime_date[2])#決済日
                            khour = int(datetime_time[0])#決済時
                            kminute = int(datetime_time[1])#決済分
                            ksecond = int(datetime_time[2])#決済秒    
                            
                            data_list.append(int(row[15])) #決済番号
                            
                            #設置場所資産番号から設置場所番号を検索
                            ret_rows = self.set_placecd(row[8])
                            data_list.append(ret_rows[0][0])      
                            
                            #明細区分番号
                            if row[2] == '現金':
                                data_list.append('1') 
                            else:
                                data_list.append('2') 
                            
                            #明細種別名称から明細種別番号を検索
                            ret_rows = self.set_meisaisyubetu(row[2])
                            data_list.append(ret_rows[0][0])             
                            
                            #決済金額(カンマ除去)
                            kingaku_str = ""
                            max_len = len(row[1])
                            kingaku = row[1]
                            if max_len >= 4:
                                for i in range(0,max_len):
                                    if kingaku[i] != ',':
                                        kingaku_str = kingaku_str + str(kingaku[i])
                            else:
                                kingaku_str = int(row[1])
                                
                            kingaku_dec = int(kingaku_str)
                            data_list.append(kingaku_dec) 
                            set_price = str(kingaku_dec)
                            sum_price += kingaku_dec                            
                            
                            #検索日付・時間セット
                            res_list = self.date_set(kyear,kmonth,kday,khour,kminute,ksecond)
                            data_list.append(res_list[0])#日付（整数）
                            #data_list.append(res_list[1])#日付（ハイフン付文字列）
                            data_list.append(res_list[2])#時間（文字列）
                            data_list.append(res_list[3])#時間（文字列） 
                            #曜日・祝日セット
                            res_list = self.week_set(kyear,kmonth,kday)
                            data_list.append(res_list[0])#曜日コード
                            data_list.append(res_list[1]) #祝日フラグ 祝日なら'1' それ以外は'0'  
                            data_list.append(res_list[2])#祝日名（空白有）
                            # 金種ラベル追加
                            data_list.append(set_price)#金種ラベル                        
                    
                            #debug 
                            #if in_count % 100 == 0:
                            #    print('データ入力件数',in_count) #100件処理毎に表示
                            in_count += 1
                            
                            #DBへの書き込み(1件ずつ書込む方式)
                            data_list2 = []
                            data_list2.append(data_list)               
                            data_num = self.data_insert2(data_list2)                         
                            #out_count +=  data_num
                            if data_num != None: 
                                out_count +=  data_num   
                            else:
                                out_err += 1   
                                                        
                            #debug 
                            #if out_count % 100 == 0: #100件処理毎に表示
                            #    print('データ出力件数',out_count)
                        else:
                            out_err += 1
                        
                    
            db_updatedate = datetime_date[0] + '-' + datetime_date[1] + '-' + datetime_date[2]
                        
            # if out_err > 0:
            #         print('入力不可件数：',out_err)
                    
            if out_count == 0 and out_err == 0:
                edit_status = 9
            else:
                edit_status = 0
                #Debug
                print('入力件数',in_count-1)
                print('出力件数',out_count)
                print('入力不可件数',out_err)
                print('合計金額',sum_price)
            
            return edit_status,out_count,db_updatedate    
    ###############################################################
    # 会社データの次回処理予定日、対象範囲を更新
    ############################################################### 
    def company_updateday_update(self,companyid):
        s_sql = f'SELECT * FROM tbcompany WHERE comcode={companyid}'
        ret_rows = self.cur.excecuteQuery(s_sql) 
        
        #次の更新日、更新期間（開始～終了）を求める
        if ret_rows[0][6] == 'day':
            days_num = int(ret_rows[0][5])
            dt1 = ret_rows[0][4] + datetime.timedelta(days=days_num) #前回更新予定日+更新間隔
            dt2 =  ret_rows[0][8] + datetime.timedelta(days=1)#前回更新終了日の翌日=新更新開始日
            dt3 = dt2 + datetime.timedelta(days=days_num-1)#新更新開始日の設定日数後=新更新最終日
    
            dt4 = datetime.date(dt1.year, dt1.month, calendar.monthrange(dt1.year, dt1.month)[1]) #新更新最終日の年付きの月末日
            
            if dt1 == dt4 and int(ret_rows[0][5]) >= 10: #次回更新予定日がその月の月末日の場合
                dt5 = dt1 + datetime.timedelta(days=1)#次回更新予定日の翌日を算出して採用
                s_sql = f"""
                    UPDATE tbcompany 
                    SET comupdate = '{dt5}',
                        comstartday = '{dt2}',
                        comendday = '{dt1}'                   
                    WHERE comcode={companyid}
                """
            else:
                 s_sql = f"""
                    UPDATE tbcompany 
                    SET comupdate = '{dt1}',
                        comstartday = '{dt2}',
                        comendday = '{dt3}'                   
                    WHERE comcode={companyid}
                """            
            ret_rows = self.cur.excecuteUpdate(s_sql)         
        
        return ret_rows #更新件数    
    ###############################################################
    # 設置場所データを設置場所コードで検索して返す
    ############################################################### 
    def place_data_get(self,placecd):
        s_sql = f'SELECT * FROM tbplace WHERE placecode={placecd}'
        ret_rows = self.cur.excecuteQuery(s_sql) 
        
        return ret_rows    
    ##############################################################
    # カード種別のデータをDataFrameで返す
    ##############################################################
    def syubetsu_get(self):
        s_sql = f'SELECT * FROM tbcard'
        ret_rows = self.cur.excecuteQuery(s_sql) 
        df_card = pd.DataFrame(ret_rows,columns =['cardcode','cardname']) 
        
        return df_card 
    ###############################################################
    # 決済区分のデータをDataFrameで返す
    ###############################################################
    def kbn_get(self):
        s_sql = f'SELECT * FROM tbkbn'
        ret_rows = self.cur.excecuteQuery(s_sql) 
        df_kbn = pd.DataFrame(ret_rows,columns =['kbncode','kbnname']) 
        
        return df_kbn
    ###############################################################
    # 設置場所のデータをDataFrameで返す
    ###############################################################
    def place_get(self):
        s_sql = f'SELECT * FROM tbplace'
        ret_rows = self.cur.excecuteQuery(s_sql) 
        df_place = pd.DataFrame(ret_rows,columns =['placecode','placename','placesisancode','placecocode'])     
        
        return df_place
    ###############################################################
    # 条件に合う取引明細データをDataFrameで返す
    # 2023.10.24 データ抽出速度向上
    ###############################################################
    def paylog_get(self,COCODE,sdate,edate): 
        sql_place = f"""  
                            SELECT placecode
                            FROM tbplace 
                            where placecocode = {COCODE}
                    """ 
        
        ret_place = self.cur.excecuteQuery(sql_place)
        #print('抽出された設置場所コード',ret_place)
        s_date = sdate.year * 10000 +  sdate.month * 100 + sdate.day
        e_date = edate.year * 10000 +  edate.month * 100 + edate.day
        
        ret_place2 = []
        for i in ret_place:
            ret_place2.append(int(i[0]))
            
        p_array = tuple(ret_place2)
        stmt = ','.join(['%s'] * len(ret_place2))
        sql_place2 = f"""
                            SELECT *
                            FROM tbpaylog as a
                            inner join tbplace as c
                                 on (a.payplacecd = c.placecode)
                            WHERE paydatedec >= '{s_date}'
                            AND paydatedec <= '{e_date}'
                            AND payplacecd IN({stmt})                            
                    """ %p_array        
        
        ret_rows = self.cur.excecuteQuery(sql_place2)
        
        colum_list = ['payyear','paymonth','payday','payhour','payminute', \
                    'paysecond','paypayno','payplacecd', 'paykbncd','paycardcd', \
                    'payprice','paydatedec','paydatestr','paytimestr', \
                    'paydatedt','paydateholidayflg','paydateholiday', 'paypricename', \
                    'placecode','placename','placesisancode','placecocode']
        df_paylog = pd.DataFrame(ret_rows,columns = colum_list) 
        #改行コード外す
        df_paylog['placecocode'] = df_paylog['placecocode'].str.strip()
        df_paylog['placesisancode'] = df_paylog['placesisancode'].str.strip()
        
        return df_paylog    
    ###############################################################
    # 月別レポート用取引明細データをDataFrameで返す    # 
    ###############################################################  
    def paylog_sum_get(self, COCODE,  edate):
        sql_place = f"""  
                            SELECT placecode
                            FROM tbplace 
                            where placecocode = {COCODE}
                    """ 
        # 指定された会社コードで設置先コード取得
        ret_place = self.cur.excecuteQuery(sql_place)
        #print('抽出された設置場所コード',ret_place)
        #s_date = sdate.year * 10000 +  sdate.month * 100 + sdate.day
        s_date = 20220501
        e_date = edate.year * 10000 +  edate.month * 100 + edate.day
        # 対象になる設置場所コードをtupleにセット
        ret_place2 = []
        for i in ret_place:
            ret_place2.append(int(i[0]))        
        #対象設置先コード、日付で売上履歴データ取得            
        p_array = tuple(ret_place2)
        stmt = ','.join(['%s'] * len(ret_place2))
        sql_place2 = f"""
                            SELECT *
                            FROM tbpaylog as a
                            inner join tbplace as c
                                 on (a.payplacecd = c.placecode)
                            WHERE paydatedec >= '{s_date}'
                            AND paydatedec <= '{e_date}'
                            AND payplacecd IN({stmt})                            
                    """ %p_array        
        
        ret_rows = self.cur.excecuteQuery(sql_place2)
        
        colum_list = ['payyear','paymonth','payday','payhour','payminute', \
                    'paysecond','paypayno','payplacecd', 'paykbncd','paycardcd', \
                    'payprice','paydatedec','paydatestr','paytimestr', \
                    'paydatedt','paydateholidayflg','paydateholiday', 'paypricename', \
                    'placecode','placename','placesisancode','placecocode']
        df_paylog = pd.DataFrame(ret_rows,columns = colum_list) 
        #改行コード外す
        df_paylog['placecocode'] = df_paylog['placecocode'].str.strip()
        df_paylog['placesisancode'] = df_paylog['placesisancode'].str.strip() 
        
        return df_paylog    
    ##############################################################
    # データベースバックアップ
    ##############################################################
    def database_backup(self,flg):

        write_to_file: bool = True
        file_name:str = 'embackup.sql'
        
        dt_now = datetime.datetime.now()
        
        dump_command = [
        'mysqldump',
        '--host=' + self.dbip,
        '--user=' + self.dbuser,
        '--password=' + self.dbpw,
        '--all-databases'
        ]
        #バックアップ実行
        dump_process = subprocess.Popen(dump_command, stdout=subprocess.PIPE,shell=True)
        #結果をsqlとして出力
        if write_to_file:
            dump_result = dump_process.communicate()[0]
            str_date = str(dt_now.month) + str(dt_now.day) + str(dt_now.hour) +  str(dt_now.minute)
            if flg == '1':
                file_name2 = str_date + '_' + 'before' + '_' + file_name 
            else:
                file_name2 = str_date + '_' + 'after'  + '_' + file_name 
            out_file_path = os.path.join(self.outpath,file_name2)    
            with open(out_file_path, 'wb') as fp:
                fp.write(dump_result) 
        
        return 0    
    ###############################################################
    # ディストラクタ
    ###############################################################
    def __del__(self):
        #print('ディストラクタ呼び出し') 
        # DBバックアップ 
        print('データベースバックアップ(処理後)開始')       
        res = self.database_backup('2')       
               