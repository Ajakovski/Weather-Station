import requests
import serial
import time

COM_PORT="COM4"
BAUD=9600
PHP_URL="http://localhost/monitoring/save_data.php"

ser=serial.Serial(COM_PORT,BAUD,timeout=2)
time.sleep(2)

while True:
    try:
        line=ser.readline().decode("utf-8").strip()
        parts=line.split(",")
        if "," in line:
            t=float(parts[0])
            h=float(parts[1])
            print(f"Temperatura: {t}*C | Vlaga: {h}%")
            respond=requests.get(PHP_URL,params={'t':t,'h':h})
    except Exception as e:
        print(f"Greska {e}")
    time.sleep(1)
        