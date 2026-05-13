import network
import time
import urequests
from machine import Pin, I2C
import onewire
import ds18x20
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

# ========== WIFI SETTINGS ==========
ssid = "Wokwi-GUEST"
password = ""

# ========== THINGSPEAK SETTINGS ==========
api_key = "YB4Q39TBT87R77ML"

# ========== PIN DEFINITIONS ==========
green = Pin(15, Pin.OUT)
yellow = Pin(14, Pin.OUT)
red = Pin(13, Pin.OUT)
buzzer = Pin(12, Pin.OUT)

# ========== DS18B20 SENSOR ==========
ds_pin = Pin(16)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
roms = ds_sensor.scan()

# ========== LCD SETUP (PICO W) ==========
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)

I2C_ADDR = 0x27  # try 0x3F if LCD not working
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

lcd.clear()
lcd.putstr("EV Battery Monitor")
time.sleep(2)
lcd.clear()

# ========== MODEL CONSTANTS ==========
Tsafe = 60.0
delta_t = 10

# ========== SENSOR CHECK ==========
if not roms:
    print("DS18B20 Sensor NOT Detected!")
    lcd.putstr("Sensor Error!")

    while True:
        red.toggle()
        buzzer.on()
        time.sleep(0.3)
        buzzer.off()
        time.sleep(0.7)

# ========== WIFI CONNECT ==========
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    print("Connecting to WiFi...")
    lcd.clear()
    lcd.putstr("Connecting WiFi")

    while not wlan.isconnected():
        time.sleep(1)

    print("Connected:", wlan.ifconfig())
    lcd.clear()
    lcd.putstr("WiFi Connected")
    time.sleep(2)
    lcd.clear()

connect_wifi()

# ========== INITIAL TEMPERATURE ==========
ds_sensor.convert_temp()
time.sleep(1)
T_prev = ds_sensor.read_temp(roms[0])

# ========== MAIN LOOP ==========
while True:

    time.sleep(delta_t)

    ds_sensor.convert_temp()
    time.sleep(1)
    T_curr = ds_sensor.read_temp(roms[0])

    # ===== SENSOR FAULT CHECK =====
    if T_curr is None or T_curr == -127:
        print("Sensor Fault Detected!")
        lcd.clear()
        lcd.putstr("Sensor Fault!")

        while True:
            red.toggle()
            buzzer.on()
            time.sleep(0.3)
            buzzer.off()
            time.sleep(0.7)

    # ===== CALCULATIONS =====
    dT_dt = (T_curr - T_prev) / delta_t
    TSI = dT_dt * (T_curr / Tsafe)

    print("Temperature:", T_curr)
    print("Rate of Rise (dT/dt):", dT_dt)
    print("TSI:", TSI)

    # ===== RISK CLASSIFICATION =====
    if (T_curr < 50) and (TSI < 0.02):
        green.on()
        yellow.off()
        red.off()
        buzzer.off()
        status = 0  # Low Risk

    elif (50 <= T_curr < 70) or (0.02 <= TSI < 0.05):
        green.off()
        yellow.on()
        red.off()
        buzzer.off()
        status = 1  # Medium Risk

    else:
        green.off()
        yellow.off()
        red.on()
        buzzer.on()
        status = 2  # High Risk

    # ===== LCD DISPLAY (NO FLICKER) =====
    lcd.move_to(0, 0)
    lcd.putstr("T:{:.1f}C TSI:{:.2f} ".format(T_curr, TSI))

    lcd.move_to(0, 1)
    if status == 0:
        lcd.putstr("SAFE      ")
    elif status == 1:
        lcd.putstr("WARNING   ")
    else:
        lcd.putstr("DANGER!   ")

    # ===== THINGSPEAK UPLOAD =====
    url = "https://api.thingspeak.com/update?api_key={}&field1={}&field2={}&field3={}".format(
        api_key, T_curr, TSI, status)

    try:
        response = urequests.get(url)
        response.close()
        print("Data sent to ThingSpeak")
    except:
        print("Upload failed")

    T_prev = T_curr
