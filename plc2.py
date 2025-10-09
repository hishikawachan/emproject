import socket
import time

host_ip = '192.168.1.199'
host_port = 8501

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((host_ip, host_port))
except:
    print("PLC connection NG")
    client.close()
    exit()

#comand = "RDS R313 3\r"
comand = "RDDM0.U\r"
#previous_water_level = 1

try:
    while True:
        client.send(comand.encode("ascii"))
        response = client.recv(64)
        response = response.decode("UTF-8")

        HH = response[0] == '1'
        H = response[2] == '1'
        L = response[4] == '1'
        
        if L and H and HH:
            waterLevel = 4
        elif L and H:
            waterLevel = 3
        elif L:
            waterLevel = 2
        else:
            waterLevel = 1

        if waterLevel != previous_water_level:
            message = str(waterLevel)
            previous_water_level = waterLevel
            print("water level:", message)

        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nfinish program")
finally:
    client.close()