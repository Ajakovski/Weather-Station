import serial
import requests
import time

COM="COM5"
BAUD=9600
PHP_URL="http://localhost/monitoring2/save_data.php"

ser=serial.Serial(COM,BAUD,timeout=2)
time.sleep(2)

while True:
    line=ser.readline().decode("utf-8").strip()
    if "," in line:
        parts=line.split(",")
        t= float(parts[0])
        h= float(parts[1])
        print(f"Temperatura: {t}*C | Vlaga: {h}%")
        result=requests.get(PHP_URL, params={"t":t,"h":h})
    time.sleep(1)