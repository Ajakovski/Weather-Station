# Smart Workstation Monitor

> Real-time temperature and humidity monitoring using Arduino, MySQL, PHP and a live web dashboard.

![Arduino](https://img.shields.io/badge/Arduino-UNO-00979D?style=for-the-badge&logo=arduino&logoColor=white)
![PHP](https://img.shields.io/badge/PHP-8.x-777BB4?style=for-the-badge&logo=php&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-monitoring-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-CSS3-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![Python](https://img.shields.io/badge/Python-bridge-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Features](#features)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [File Explanations](#file-explanations)
- [Testing and Verification](#testing-and-verification)
- [Troubleshooting](#troubleshooting)
- [Grading Criteria](#grading-criteria)
- [License](#license)

---

## Overview

The **Smart Workstation Monitor** is a full-stack IoT project that reads ambient temperature and humidity data from a DHT11 sensor connected to an Arduino UNO, stores the measurements in a MySQL database via a PHP API, and displays them in real time through a self-refreshing web dashboard.

This project was developed as a practical exam for the **Electrotechnician for Computer Technology and Automation** vocational programme, covering all 8 assessed areas: planning, hardware assembly, networking, programming, robotics, databases, user support, and workplace safety.

---

## System Architecture

```
+-------------+    Serial/USB    +--------------+    HTTP GET    +-----------------+
|   DHT11     | ---------------> |  bridge.py   | ------------> |  save_data.php  |
|   Sensor    |                  |  (Python)    |               |  (PHP + Apache) |
+-------------+                  +--------------+               +--------+--------+
      |                                                                   |
      v                                                                   v
+-------------+                                                 +-----------------+
|  Arduino    |                                                 |  MySQL Database |
|  UNO        |                                                 |  (monitoring)   |
+-------------+                                                 +--------+--------+
                                                                         |
                                                                         v
                                                              +---------------------+
                                                              |  index.html         |
                                                              |  (Live Dashboard)   |
                                                              |  auto-refresh: 5s   |
                                                              +---------------------+
```

**Data flow:**
DHT11 reads -> Arduino formats -> USB Serial -> Python bridge -> PHP API -> MySQL -> HTML dashboard

---

## Features

- **Live sensor readings** - temperature (C) and humidity (%) every 2 seconds
- **Persistent storage** - all measurements saved to MySQL with automatic timestamps
- **Web dashboard** - auto-refreshing HTML/CSS/JS interface, no page reload needed
- **Secure backend** - SQL injection protection via Prepared Statements, input validation
- **Python bridge** - decoupled Serial-to-HTTP middleware for clean architecture
- **History table** - last 20 measurements displayed with date and time
- **Status indicator** - animated live indicator shows system connectivity
- **Error handling** - NaN detection on Arduino, HTTP error codes from PHP

---

## Hardware Requirements

| Component | Specification | Notes |
|-----------|--------------|-------|
| Microcontroller | Arduino UNO | ESP32 also compatible |
| Sensor | DHT11 or DHT22 | DHT22 = higher accuracy |
| Resistor | 10k ohm pull-up | Between DATA and VCC |
| Breadboard | Standard 830-point | |
| Jumper wires | M-M, min. 3 | Red, Yellow, Black |
| USB Cable | Type A to Type B | Standard Arduino cable |
| Computer | Windows / Linux / macOS | Runs XAMPP + Python |

### Wiring Diagram

```
DHT11 Pin         Arduino UNO Pin     Wire Color
-------------------------------------------------
VCC  (Pin 1)  --> 5V                  RED
DATA (Pin 2)  --> D2 (Digital 2)      YELLOW
NC   (Pin 3)      (not connected)
GND  (Pin 4)  --> GND                 BLACK

Optional: 10k ohm resistor between DATA and VCC for signal stability
```

---

## Software Requirements

| Software | Version | Purpose | Download |
|----------|---------|---------|----------|
| XAMPP | 8.x | Apache + MySQL server | apachefriends.org |
| Arduino IDE | 2.x | Upload code to Arduino | arduino.cc |
| Python | 3.8+ | Serial-to-HTTP bridge | python.org |
| VS Code | Latest | Code editor (optional) | code.visualstudio.com |

**Python packages required:**
```bash
pip install pyserial requests
```

**Arduino libraries required** (via Arduino IDE -> Manage Libraries):
- `DHT sensor library` by Adafruit
- `Adafruit Unified Sensor`

---

## Project Structure

```
smart-workstation-monitor/
|
+-- arduino_dht11.ino       # Arduino sketch - reads DHT11, sends via Serial
+-- bridge.py               # Python bridge - Serial to HTTP to PHP
+-- database_setup.sql      # MySQL schema - creates database and table
+-- save_data.php           # PHP API - receives data, queries MySQL
+-- index.html              # Web dashboard - displays live readings
+-- README.md               # This file
```

---

## Installation and Setup

Follow these steps **in order**. Do not skip any phase.

### Phase 1 - Install Software

1. Install **XAMPP** and start both **Apache** and **MySQL** (both green in Control Panel)
2. Install **Arduino IDE** and add libraries: `DHT sensor library` + `Adafruit Unified Sensor`
3. Install **Python 3** and make sure to tick **"Add Python to PATH"** during setup
4. Open a terminal and run:

```bash
pip install pyserial requests
```

---

### Phase 2 - Set Up the Database

1. Open your browser and go to `http://localhost/phpmyadmin`
2. Click the **SQL** tab
3. Open `database_setup.sql`, copy all contents, paste into the SQL field, click **Go**
4. You should see a new database **monitoring** with a table **senzori** in the left panel

**Table structure:**

| Column | Type | Description |
|--------|------|-------------|
| `id` | INT AUTO_INCREMENT | Unique record ID (automatic) |
| `temperatura` | DECIMAL(5,2) | Temperature in degrees C |
| `vlaga` | DECIMAL(5,2) | Relative humidity in percent |
| `vreme` | DATETIME | Timestamp (automatic) |

---

### Phase 3 - Deploy Web Files

Copy these two files into `C:\xampp\htdocs\monitoring\`:

```
C:\xampp\htdocs\monitoring\
    +-- save_data.php
    +-- index.html
```

> Note: `arduino_dht11.ino`, `bridge.py`, and `database_setup.sql` are NOT placed here.

Verify PHP is working by visiting:
```
http://localhost/monitoring/save_data.php?action=last
```

Expected response:
```json
{"status":"ok","data":[{"id":"1","temperatura":"22.50","vlaga":"54.30","vreme":"2025-03-01 10:00:00"}]}
```

---

### Phase 4 - Upload Arduino Code

1. Wire the DHT11 to Arduino (disconnect USB first)
2. Reconnect USB, open Arduino IDE
3. Open `arduino_dht11.ino`
4. Set board: `Tools -> Board -> Arduino UNO`
5. Set port: `Tools -> Port -> COM3` (or whichever port appears)
6. Click **Upload** and wait for `Done uploading`
7. Open **Serial Monitor** (Ctrl+Shift+M), set baud to **9600**
8. You should see values every 2 seconds:

```
Sistem pokrenat. Citanje na temperatura i vlaga...
23.50,55.30
23.60,55.10
```

---

### Phase 5 - Run the Python Bridge

> **Important:** Close Serial Monitor in Arduino IDE before this step. Both cannot use the COM port simultaneously.

1. Open `bridge.py` and set your COM port:

```python
COM_PORT = "COM3"   # Change to your port
```

2. Run the bridge:

```bash
python bridge.py
```

3. Expected output:

```
Connecting to COM3 at 9600 baud...
Connected! Reading data...
Temperature: 23.50 C | Humidity: 55.30%
  -> Response: {"status": "ok", "id": 2}
```

---

### Phase 6 - Open the Dashboard

With XAMPP and `bridge.py` both running, open:

```
http://localhost/monitoring/index.html
```

The dashboard will show live temperature, humidity, and a scrolling history table, refreshing every **5 seconds** automatically.

---

## File Explanations

### arduino_dht11.ino

The Arduino sketch. It initializes the DHT11 sensor and opens a 9600-baud Serial connection. The `loop()` function runs forever: it waits 2 seconds, reads temperature and humidity as floats, checks for invalid readings using `isnan()`, and prints them as `temperature,humidity` over USB. This is the hardware layer of the system.

### database_setup.sql

A SQL script that creates the `monitoring` database and the `senzori` table. The `id` field auto-increments so each record is uniquely identified without manual input. `DECIMAL(5,2)` stores values like `23.50` or `-5.30`. The `vreme` field uses `DEFAULT CURRENT_TIMESTAMP` so the time of each measurement is recorded automatically by MySQL.

### save_data.php

The PHP backend API with two modes:
- `?t=23.5&h=55.3` - validates and stores a new measurement
- `?action=last` - returns the last 20 records as JSON

It uses Prepared Statements to prevent SQL injection, validates that temperature is within -40 to 80 degrees C and humidity within 0-100%, and returns JSON responses with HTTP status codes for errors.

### bridge.py

The middleware connecting the hardware to the web stack. It opens the Arduino's Serial port, reads lines in the format `t,h`, parses them into floats, and forwards them to `save_data.php` via HTTP GET using the `requests` library. It runs in an infinite loop and handles exceptions gracefully so a single bad read does not crash the process.

### index.html

A single-file web app combining HTML structure, CSS styling, and JavaScript logic. The `fetchData()` function calls `save_data.php?action=last` via the `fetch()` API, parses the JSON, and updates the temperature/humidity cards and history table in the DOM. `setInterval(fetchData, 5000)` re-runs this every 5 seconds. A CSS `@keyframes` animation pulses the status dot to indicate the system is live.

---

## Testing and Verification

Use this checklist to verify the full system end-to-end:

| # | What to check | How to check | Expected result |
|---|--------------|--------------|-----------------|
| 1 | XAMPP running | XAMPP Control Panel | Apache + MySQL green |
| 2 | Database exists | phpMyAdmin -> monitoring | Table `senzori` visible |
| 3 | PHP API reachable | Browser -> `.../save_data.php?action=last` | JSON response |
| 4 | Arduino sending data | Arduino IDE Serial Monitor | `23.50,55.30` every 2s |
| 5 | Bridge forwarding | Terminal running bridge.py | `status: ok` per reading |
| 6 | Dashboard live | Browser -> `.../index.html` | Cards and table updating |

**Manual test without Arduino** - simulate a reading by visiting:
```
http://localhost/monitoring/save_data.php?t=25.0&h=65.0
```
Then refresh `index.html` to confirm the value appears in the table.

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `avrdude: ser_open(): can't open device` | Wrong COM port | Try Tools -> Port -> different COM |
| Serial Monitor shows `GRESKA: Neuspesno` | Bad wire on DATA pin | Re-check D2 wiring |
| `serial.SerialException` in bridge.py | COM port busy | Close Arduino IDE Serial Monitor |
| PHP returns `Access denied` | Wrong MySQL credentials | Set `$db_pass = ""` in save_data.php |
| Dashboard shows `--` values | bridge.py not running | Start bridge.py in a terminal |
| `Port 80 already in use` in XAMPP | Another app on port 80 | Change Apache to port 8080 in XAMPP Config |
| `Table doesn't exist` error | SQL script not executed | Redo Phase 2 in phpMyAdmin |

---

## Grading Criteria

This project fulfils all 8 assessed areas totalling **100 points**:

| Area | Topics Covered | Points |
|------|---------------|--------|
| Planning and Organisation | Work plan, equipment check, standards | 10 |
| Assembly and Maintenance | DHT11 wiring, verification, industry standards | 15 |
| Computer Networks | Serial + HTTP architecture, IP configuration | 15 |
| Programming and Automation | Arduino code, error handling, documentation | 15 |
| Robotics and Intelligent Systems | Autonomous operation, state diagram | 15 |
| Databases and Web Technologies | MySQL schema, PHP API, HTML/CSS/JS | 10 |
| User Support | Setup guide, troubleshooting table | 10 |
| Safety and Security | ESD precautions, GDPR, safety rules | 10 |
| **Total** | | **100** |

---

## License

This project is released under the [MIT License](https://opensource.org/licenses/MIT) - free to use, modify, and distribute with attribution.

---

*Built for the Electrotechnician for Computer Technology and Automation practical exam - 2024/2025*