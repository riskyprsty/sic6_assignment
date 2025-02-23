import time
import camera
import ubinascii
import urequests
import network

SSID = "Realme GT Neo 3"
PASSWORD = "qwertyuiop1"
SERVER_URL = "http://192.168.249.119:5000/upload" 

"""
ESP32 MICROPYTHON UBIDOTS PROJECT
-- The Hash Slinging Slasher --
-- UNI022 --
-- PENS --

Assignment Samsung Innovation Campus 6
"""

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)
while not wifi.isconnected():
    time.sleep(1)

print("Terhubung ke WiFi:", wifi.ifconfig())

camera.init(0, format=camera.JPEG)
camera.framesize(camera.FRAME_VGA)
camera.quality(10)

while True:
    img = camera.capture()
    if img:
        img_base64 = ubinascii.b2a_base64(img).decode('utf-8')  
        data = {"image": img_base64}  

        try:
            print("Mengirim gambar ke server...")
            response = urequests.post(SERVER_URL, json=data)
            print("Respon server:", response.text)
            response.close()
        except Exception as e:
            print("Gagal mengirim gambar:", str(e))

    time.sleep(5)
