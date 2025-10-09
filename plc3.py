import socket

host = "192.168.1.199"
port = 8501

TCP_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   #TCP通信
#TCP_client.settimeout(10)
TCP_client.connect((host, port))

#UDP_client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)   #UDP通信
#UDP_client.settimeout(10)
#UDP_client.connect((host, port))

# コマンド通信処理



# ================= KV Series TCP and UDP ===================== #
# ASCII 通信
# 読出し例
# RDS(\x20)(デバイス種別)(デバイス番号)(データ形式)(\x20)(読出し個数)(\x0D)
# データメモリ8000番の場合
# b"RDS\x20DM008000.U\x200002\x0D"
# 書込み例
# WRS(\x20)(デバイス種別)(デバイス番号)(データ形式)(\x20)(書込み個数)(\x20)(データ1)(\x20)(データ2)(\x20)...(\x0D)
# データメモリ8000番の場合
# b"WRS\x20DM008000.U\x200002\x20AA\x20BB\x0D"

# ZFレジスタの場合
# b"RDS\x20ZF061100.U\x201\x0D"
# b"WRS\x20ZF061104.U\x201\x202\x0D"

# ================= 通信例 ================= #
command = b"RDS\x20DM000001.U\x200002\x0D"
#送信
TCP_client.send(bytes(command))
#受信
response = TCP_client.recv(1024)
#受信文変換
data_sum = ""
for dt in response[:-2]:
    temp = chr(int(format(dt, "02X"), 16))
    data_sum = data_sum + temp 

#return_data = int(data_sum)
print('return =',data_sum)

# コマンド通信処理
TCP_client.close()
