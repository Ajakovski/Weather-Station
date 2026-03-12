import requests
import time
import serial

COM_PORT="COM4"
BAUD=9600
PHP_URL="http://localhost/monitoring/save_data.php"

ser=serial.Serial(COM_PORT,BAUD,timeout=2)
time.sleep(2)
print("Uspesno povrzana")

while True:
    try:
        line=ser.readline().decode("utf-8").strip()
        if "," in line:
            parts=line.split(",")
            t=float(parts[0])
            h=float(parts[1])
            print(f"")
            response=requests.get(PHP_URL,params={"t":t,"h":h})
    except Exception as e:
        print(f"Greska: {e}")
    time.sleep(1)