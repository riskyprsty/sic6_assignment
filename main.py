from umqtt.robust import MQTTClient
from time import sleep, sleep_ms
from hcsr04 import HCSR04
from lib.micropyGPS import MicropyGPS
import machine as m
import dht

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
sensorDht = dht.DHT11(m.Pin(15))
sensorUltraSonic = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)
led = m.Pin(27, m.Pin.OUT)
pin13 = m.Pin(13, m.Pin.IN, m.Pin.PULL_UP)

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


def main():
    while True:
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
                        
                        msg = b'{"location": {"value":%s, "context":{"lat":%s, "lng":%s}}, "sattelite": {"value":%s}, "altitude": {"value":%s}, "temperature": {"value":%s}, "humidity": {"value":%s}, "distance": {"value":%s}}' % (var, lat, lon, sat, alt, temp, hum, dist)
                        
                        client.publish(b"/v1.6/devices/ESP32_THSS", msg)

                        print('---------------------------------')
                        print('UTC Timestamp:', my_gps.timestamp)
                        print('Date:', my_gps.date_string('long'))
                        print(f"Latitude: {lat:.6f}, Longitude: {lon:.6f}")
                        print('Altitude:', my_gps.altitude)
                        print('Satellites in use:', my_gps.satellites_in_use)
                        print('HDOP:', my_gps.hdop)
                        print('Temperature: %3.1f C' %temp)
                        print('Humidity: %3.1f %%' %hum)
                        print()
                
        except Exception as e:
            print(f"An error occurred: {e}")
            
        checkwifi()
        client.check_msg()
        sleep(2)
    
main()   