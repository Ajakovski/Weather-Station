import serial 
import requests #pip install pyserial requests
import time
#py -3.14 bridge.py
#python bridge.py
# === ПОСТАВКИ — Промени ги ако е потребно ===
COM_PORT  = "COM4"          # Промени во твојот COM порт (COM3, COM4, COM5...)
BAUD_RATE = 9600            # Мора да совпаѓа со Arduino кодот
PHP_URL   = "http://localhost/monitoring/save_data.php"

print(f"Поврзување на {COM_PORT} со {BAUD_RATE} baud...")
ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=2)
time.sleep(2)  # Чекај Arduino да се ресетира по поврзување
print("Поврзано! Читање на податоци...")

while True:
    try:
        line = ser.readline().decode("utf-8").strip()
        if "," in line:
            parts = line.split(",")
            t = float(parts[0])
            h = float(parts[1])
            print(f"Температура: {t}°C | Влага: {h}%")
            # Испрати до PHP скриптата
            response = requests.get(PHP_URL, params={"t": t, "h": h})
            print(f"  -> Одговор: {response.json()}")
    except Exception as e:
        print(f"Грешка: {e}")
    time.sleep(1)
