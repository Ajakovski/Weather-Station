import serial
import requests
import time

PORT = "COM3"
BAUD=9600
PHP_URL="http://localhost/monitoring/save_data.php"

print(f"Povrzuvanje na {PORT} so {BAUD} baud...")
ser=serial.Serial(PORT,BAUD,timeout=2)
time.sleep(2)

while True:
    try:
        line=ser.readline().decode("utf-8").strip()
        if "," in line:
            parts=line.split(",")
            t=float(parts[0])
            h=float(parts[1])
            print(f"Temperatura {t}*C, Vlaznost {h}%")
            response=requests.get(PHP_URL,params={"t": t,"h":h})
    except Exception as e:
        print(f"Greska {e}")
    time.sleep(1)