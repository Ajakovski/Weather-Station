import serial
import requests
import time

COM_PORT= "COM4"
BAUD_RATE= 9600
PHP_URL="http://localhost/monitoring/save_data.php"

#print(f"Povrzuvanje na {COM_PORT} cc {BAUD_RATE} baud...")
ser=serial.Serial(COM_PORT, BAUD_RATE, timeout=2)
time.sleep(2)
#print("Povrzano! Citame podatoci...")

while True:
    line =ser.readline().decode("utf-8").strip()
    if "," in line:
        parts= line.split(",")
        t=float(parts[0])
        h=float(parts[1])
        #print(f"Temperatura: {t} C, Vlaga: {h} %")
        response=requests.get(PHP_URL, params={"t": t, "h": h})
        #print(f" -> Odgovor: {response.json()}")
    time.sleep(1)
        