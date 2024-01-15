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
# ======================================
from datetime import datetime
import datetime
import calendar
import os
from dateutil.relativedelta import relativedelta
import jpholiday
import subprocess
import pandas as pd
from emoneydbaccess import dbAccessor
import emoneyweather as ew

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
    def __init__(self,parm_list):
        # DB接続
        self.cur = dbAccessor(parm_list[1], parm_list[2], parm_list[0], parm_list[3], parm_list[4])
        self.dbip = parm_list[0]
        self.dbmarianame = parm_list[1]
        self.dbport = parm_list[2]        
        self.dbuser = parm_list[3]
        self.dbpw = parm_list[4]
        self.filepath = parm_list[5]
        
    #####################################
    # テーブル名一覧を取得
    #####################################
    def tabele_name_list_get(self):
        ret_list = self.cur.table_name_get()
        return ret_list
    
    #####################################
    # データ存在チェック(売上照会系)
    #####################################
    def db_wcheck1(self,data_list):
        check_sql = f"""    
                SELECT * 
                FROM    tbpaylog
                WHERE   payyear = {data_list[0]}
                AND     paymonth = {data_list[1]}
                AND     payday = {data_list[2]}
                AND     payhour = {data_list[3]}
                AND     payminute = {data_list[4]}
                AND     paysecond = {data_list[5]}
                AND     paypayno = {data_list[6]}
                AND     payplacecd = {data_list[7]}
                AND     payprice = {data_list[10]}    
        """
        rows = self.cur.excecuteQuery(check_sql)
        return rows
    #####################################
    # データ存在チェック(売上照会系以外)
    #####################################
    def db_wcheck2(self,data_list):
        check_sql = f"""    
                SELECT * 
                FROM    tbpaylog
                WHERE   payyear = {data_list[0]}
                AND     paymonth = {data_list[1]}
                AND     payday = {data_list[2]}
                AND     payhour = {data_list[3]}
                AND     payminute = {data_list[4]}
                AND     paysecond = {data_list[5]}
                AND     payplacecd = {data_list[7]}
                AND     payprice = {data_list[10]}    
        """
        rows = self.cur.excecuteQuery(check_sql)
        return rows
    ####################################    
    #　実データ書き込み
    ####################################
    def data_insert(self,row):
        output_sql = """
            INSERT INTO tbpaylog
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                   %s, %s, %s, %s, %s, %s)
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
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                   %s, %s, %s, %s, %s, %s)
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
        #debug
        #print('削除件数: ',num)
        #debug
        # 最新データ出力
        output_sql = """
            INSERT INTO tbweather
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                
        """
        num2 = self.cur.excecuteInsertmany(output_sql,data_list) 
        #debug
        #print('出力件数: ',num)
        #debug         

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
        #debug
        #print('設置場所番号抽出開始：',datetime.datetime.now())   
        
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
                    'paydatedt','paydateholidayflg','paydateholiday', \
                    'placecode','placename','placesisancode','placecocode']
        df_paylog = pd.DataFrame(ret_rows,columns = colum_list) 
        #改行コード外す
        df_paylog['placecocode'] = df_paylog['placecocode'].str.strip()
        df_paylog['placesisancode'] = df_paylog['placesisancode'].str.strip()
        
        #debug
        #print('設置場所番号抽出終了：',datetime.datetime.now()) 
        
        # # 対象日付及び対象会社で抽出(廃止)
        # df_paylog = df_paylog.astype({'payyear':int,'paymonth': int,'payday':int,'placecocode':str})   
        
        # s_date = sdate.year * 10000 +  sdate.month * 100 + sdate.day
        # e_date = edate.year * 10000 +  edate.month * 100 + edate.day
        
        # df_paylog1 = df_paylog[(df_paylog['paydatedec'] >= s_date) & (df_paylog['paydatedec'] <= e_date) & (df_paylog['placecocode'] == COCODE)]   
        
        return df_paylog
    ###############################################################
    # 条件に合う取引明細データの売上金額を年・月で集計
    ###############################################################
    # def paylog_sum_get(self,COCODE,sdate,edate):  
    #     syear = sdate.year
    #     eyear = edate.year
    #     smonth = sdate.month
    #     emonth = edate.month        
    #     years = edate.year - sdate.year
    #     if years < 2 and years >=0:    #2年以上のデータは対象外
    #         sql_paylog = f"""  
    #                             SELECT *
    #                             FROM tbpaylog as a
    #                             inner join tbplace as c
    #                                 on (a.payplacecd = c.placecode)
    #                     """
    #         #debug
    #         print('売上履歴データ処理２開始：',datetime.datetime.now())   
            
    #         ret_rows = self.cur.excecuteQuery(sql_paylog) 
            
    #         #debug
    #         print('売上履歴データ処理２終了：',datetime.datetime.now())   
            
    #         colum_list = ['payyear','paymonth','payday','payhour','payminute', \
    #                     'paysecond','paypayno','payplacecd', 'paykbncd','paycardcd', \
    #                     'payprice','paydatedec','paydatestr','paytimestr', \
    #                     'paydatedt','paydateholidayflg','paydateholiday', \
    #                     'placecode','placename','placesisancode','placecocode']       
            
    #         df_paylog = pd.DataFrame(ret_rows,columns = colum_list)
    #         #改行コード外す
    #         df_paylog['placecocode'] = df_paylog['placecocode'].str.strip() 
    #         df_paylog = df_paylog.astype({'payyear':int,'paymonth': int}) 
            
    #         df_paylog = df_paylog[(df_paylog['placecocode'] == COCODE)] #会社コード抽出 
            
    #         if syear < eyear:            
    #             df_paylog1 = df_paylog[(df_paylog['payyear'] == syear) & (df_paylog['paymonth'] >= smonth)]#開始年と等しく、開始月以上
    #             df_paylog3 = df_paylog[(df_paylog['payyear'] == eyear) & (df_paylog['paymonth'] <= emonth)]#終了年と等しく、終了月以下
    #             df_paylog5 = pd.concat([df_paylog1, df_paylog3])              
    #         else:
    #             if syear == eyear:
    #                 df_paylog5 = df_paylog[(df_paylog['paymonth'] >= sdate.month) & (df_paylog['paymonth'] <= edate.month)] #開始月以上、終了月以下
 
    #         df_paylog6 = pd.pivot_table(df_paylog5, index=['placename'], columns=['payyear','paymonth'],values=['payprice'],aggfunc='sum',margins=True,margins_name='Total')  #クロス集計 
    #     else:
    #         ret_rows = [9,]    
    #         df_paylog6 = pd.DataFrame(ret_rows,columns = 'errcode')
        
    #     return df_paylog6
    
    def paylog_sum_get(self,COCODE,sdate,edate):
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
                    'paydatedt','paydateholidayflg','paydateholiday', \
                    'placecode','placename','placesisancode','placecocode']
        df_paylog = pd.DataFrame(ret_rows,columns = colum_list) 
        #改行コード外す
        df_paylog['placecocode'] = df_paylog['placecocode'].str.strip()
        df_paylog['placesisancode'] = df_paylog['placesisancode'].str.strip()
        
        #df_paylog = pd.pivot_table(df_paylog, index=['placename'], columns=['payyear','paymonth'],values=['payprice'],aggfunc='sum',margins=True,margins_name='Total')   
        #df_paylog = pd.pivot_table(df_paylog, index=['payyear','paymonth'], columns=['placename'],values=['payprice'],aggfunc='sum',margins=True,margins_name='Total') 
        
        return df_paylog
    
    ##############################################################
    # データベースバックアップ
    ##############################################################
    def database_backup(self):

        write_to_file: bool = True
        file_name:str = 'emoneybackup.sql'
        
        dt_now = datetime.datetime.now()
        
        dump_command = [
        'mysqldump',
        '--host=' + self.dbip,
        '--user=' + self.dbmarianame,
        '--password=' + self.dbpw,
        '--all-databases'
        ]
        #バックアップ実行
        dump_process = subprocess.Popen(dump_command, stdout=subprocess.PIPE,shell=True)
        #結果をsqlとして出力
        if write_to_file:
            dump_result = dump_process.communicate()[0]
            str_date = str(dt_now.month) + str(dt_now.day) + str(dt_now.hour) +  str(dt_now.minute)
            file_name2 = str_date + '_' + file_name
            out_file_path = os.path.join(self.filepath,file_name2)    
            with open(out_file_path, 'wb') as fp:
                fp.write(dump_result) 
        
        return 0
    
    ###############################################################
    # ディストラクタ
    ###############################################################
    def __del__(self):
        #print('ディストラクタ呼び出し') 
        pass 
               