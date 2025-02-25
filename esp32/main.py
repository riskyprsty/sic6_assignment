from umqtt.robust import MQTTClient
from time import sleep, sleep_ms
from hcsr04 import HCSR04
from lib.micropyGPS import MicropyGPS
import urequests as requests
import machine as m
import dht
import ssd1306
import ujson

"""
ESP32 MICROPYTHON UBIDOTS PROJECT
-- The Hash Slinging Slasher --
-- UNI022 --
-- PENS --

Assignment Samsung Innovation Campus 6
"""

ubidotsToken = "BBUS-09DidGsAEKGqkJ7U76nm3btnWFjgHP"
clientID = "esp32wroom32"
client = MQTTClient("clientID", "industrial.api.ubidots.com", 1883, user = ubidotsToken, password = ubidotsToken)

my_gps = MicropyGPS()
gps_serial = m.UART(2, baudrate=9600, tx=17, rx=16)
sensorDht = dht.DHT22(m.Pin(15))
sensorUltraSonic = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)
led = m.Pin(27, m.Pin.OUT)
pin13 = m.Pin(13, m.Pin.IN, m.Pin.PULL_UP)

i2c = m.SoftI2C(scl=m.Pin(22), sda=m.Pin(21))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)


def convert_to_decimal(degrees, direction):
    decimal = degrees[0] + (degrees[1] / 60)
    if direction in ('S', 'W'):
        decimal = -decimal
    return decimal

def led_cb(topic, msg):
    print((topic, msg))
    if msg.decode() == '1.0':
        print("LED ON")
        led.value(1)
    else:
        print("LED OFF")
        led.value(0)

try:
    client.connect()
except Exception as e:
    print("Error: ", e)
    
try:
    client.set_callback(led_cb)
    client.subscribe(b"/v1.6/devices/esp32_thss/led/lv")
except Exception as e:
    print("Error: ", e)
    
def checkwifi():
    while not sta_if.isconnected():
        sleep_ms(500)
        print(".")
        sta_if.connect()

def send_data(var, lat, lon, sat, alt, temp, hum, dist):
    
    HEADERS = {
            "Content-Type": "application/json"
        }
    data = {
        "data_sensor": {
            "location": {
                "value": var,
                "context": {
                    "lat": lat,
                    "lng": lon
                }
            },
            "satellite": {
                "value": sat
            },
            "altitude": {
                "value": alt
            },
            "temperature": {
                "value": temp
            },
            "humidity": {
                "value": hum
            },
            "distance": {
                "value": dist
            }
        }
    }

    
    results = requests.post("http://sic6.tribone.my.id/insert_data_one", json=(data),headers=HEADERS)
    print(results.text)
    results.close()


# def ppppppp():
#     results = requests.get("http://192.168.0.101:5000")
#     print(results.text)
#     results.close()

    
def main():
    while True:
        # ppppppp()
        try:
            sensorDht.measure()
            temp = sensorDht.temperature()
            hum = sensorDht.humidity()
            dist = sensorUltraSonic.distance_cm()
            while gps_serial.any():
                data = gps_serial.read()
                
                for byte in data:
                    status = my_gps.update(chr(byte))
                    if status is not None:
                        lat = convert_to_decimal(my_gps.latitude, my_gps.latitude[2])
                        lon = convert_to_decimal(my_gps.longitude, my_gps.longitude[2])
                        sat = my_gps.satellites_in_use
                        alt = my_gps.altitude
                        var = repr(pin13.value())
                        oled.fill(0)
                        msg = b'{"location": {"value":%s, "context":{"lat":%s, "lng":%s}}, "sattelite": {"value":%s}, "altitude": {"value":%s}, "temperature": {"value":%s}, "humidity": {"value":%s}, "distance": {"value":%s}}' % (var, lat, lon, sat, alt, temp, hum, dist)
                        # print(msg)
                        client.publish(b"/v1.6/devices/ESP32_THSS", msg)
                        oled.text("Temp: %3.1f C" % temp, 0, 0)
                        oled.text("Hum: %3.1f %%" % hum, 0, 10)
                        oled.text("Dist: %3.1f cm" % dist, 0, 20)
                        oled.text("Sat: %d  Alt: %3.1f m" % (sat, alt), 0, 30)
                        oled.text("Lat: %3.6f" % lat, 0, 40)
                        oled.text("Lon: %3.6f" % lon, 0, 50)
                        oled.text("Var: %s" % var, 0, 60)
                        oled.show()
                        
                        print('---------------------------------')
                        print('UTC Timestamp:', my_gps.timestamp)
                        print('Date:', my_gps.date_string('long'))
                        print(f"Latitude: {lat:.6f}, Longitude: {lon:.6f}")
                        print('Altitude:', my_gps.altitude)
                        print('Satellites in use:', my_gps.satellites_in_use)
                        print('HDOP:', my_gps.hdop)
                        print('Temperature: %3.1f C' %temp)
                        print('Humidity: %3.1f %%' %hum)
                        send_data(var, lat, lon, sat, alt, temp, hum, dist)
                        # tes()
                        
                
        except Exception as e:
            print(f"An error occurred: {e}")
            
        checkwifi()
        client.check_msg()
        sleep(2)
    
main()   