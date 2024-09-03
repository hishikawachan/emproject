
import csv
import datetime
from datetime import datetime as dt
output_cnt = 0
input_cnt = 0
chg_cnt = 0
chg1_cnt = 0
chg5_cnt = 0
output_data = []
input_filepath = r'C:\Users\hishi\OneDrive\Workplace\emoney\incomes_0000001.csv'
output_filepath = r'C:\Users\hishi\OneDrive\Workplace\emoney\incomes_0000001_out.csv'
code1 = '0000001-5'
code2 = '0000001-1'
com1_date = datetime.datetime(2024, 8, 30, 14, 1, 29)

with open(input_filepath, encoding = 'UTF-8-sig') as fin:
    reader = csv.reader(fin)
    for row in reader :
        input_data = []
        # row[0]売上日時が2024/8/30 14:01:29以上の場合
        # row[8]AM機器管理番号が'0000001-5'は'0000001-1'に変更
        # row[9]AM機器名        'ボールベンダー2号機'に変更
        # row[11]端末識別番号を1に変更
        # row[16][17][18]を1Fに変更
        #        同            '0000001-1'は'0000001-5'に変更
        #                      'ボールベンダー4号機'に変更
        # row[11]端末識別番号を5に変更
        # row[16][17][18]を2Fに変更
        if row[1] == '金額':
            # headerの出力
            for i in range(0,22):
                input_data.append(row[i])
            output_data.append(input_data)
        else:
            input_cnt += 1
            tdatetime = dt.strptime(row[0], '%Y-%m-%d %H:%M:%S')
            if tdatetime >= com1_date:
                #print('対象')
                for i in range(0,8):
                    input_data.append(row[i])
                if row[8] == '0000001-5':
                    input_data.append('0000001-1')
                    chg1_cnt += 1
                else:
                    if row[8] == '0000001-1':
                        input_data.append('0000001-5')
                        chg5_cnt += 1
                    else:
                        input_data.append(row[8])
                for i in range(9,22):
                    input_data.append(row[i])
                chg_cnt += 1
            else:
                for i in range(0,22):
                    input_data.append(row[i])

            output_data.append(input_data)
            output_cnt += 1

#output_data.append(input_data)
        
with open(output_filepath, 'w',  newline='', encoding = 'UTF-8-sig') as fout:
    writer = csv.writer(fout)
    for row in output_data:
        writer.writerow(row)     

    print('総入力件数 input =',input_cnt)
    #print('chg_cnt = ',chg_cnt)
    print('2号機に変更した件数 chg1_cnt = ',chg1_cnt)
    print('5号機に変更した件数 chg5_cnt = ',chg5_cnt)
    #print('output =',output_cnt)



