from datetime import datetime
import pandas as pd 

date_int1 = 2025020306510220 / 100
date_int2 = round(date_int1)
date_str = str(date_int2)

# 月のゼロ取り
if date_str[4:5] == '0':
    date_str_month = date_str[5:6]
else:
    date_str_month = date_str[4:6]

# 日のゼロ取り
if date_str[6:7] == '0':
    date_str_day = date_str[7:8]
else:
    date_str_day = date_str[6:8]

# 時間のゼロ取り
if date_str[8:9] == '0':
    date_str_hour = date_str[9:10]
else:
    date_str_hour = date_str[8:10]

# 分のゼロ取り
if date_str[10:11] == '0':
    date_str_min = date_str[11:12]
else:
    date_str_min = date_str[10:12]

date_str_sec = date_str[12:14]

datetime_str = date_str[0:4] + '/' +  date_str_month + '/' +  date_str_day + ' ' + date_str_hour + ':' + date_str_min + ':' + date_str_sec

print(datetime_str)

"""
datetime_type = pd.to_datetime(str(date_int2))


date_str2 = '2025/2/9  9:57:58'
print(type(date_str2))

print(datetime_type)
print(type(datetime_type))
"""
