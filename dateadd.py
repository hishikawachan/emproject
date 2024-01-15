from datetime import datetime
import datetime
import os
from emdbclass import DataBaseClass
import emweather as ew

#データベース操作クラス初期化
resdb = DataBaseClass() 

ret_tuple = []
ret_rows = []
ret_tuple = resdb.weather_get2()

# 気象データテーブルに日付項目を追加 2023.11.8
# for i in ret_tuple:
#     create_date = datetime.datetime(int(i[5]),int(i[6]),int(i[0]),0,0,0)
#     result = resdb.weather_update(create_date,i[0],i[5],i[6])
#     print('date',create_date)

# s_date = datetime.datetime(2023,10,30,0,0,0)
# e_date = datetime.datetime(2023,11,5,23,59,59)

prec = 46
block = 47670
year = 2023
month = 10

# ret_tuple = resdb.weather_get3(s_date, e_date, prec, block)
# for row in ret_tuple:
#     print('test', row[5])

ret_rows = ew.weather_list_get(prec,block,year,month)

ret = resdb.weather_data_output(prec,block,year,month)

print('end')





