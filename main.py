from umqtt.robust import MQTTClient
from time import sleep, sleep_ms
from hcsr04 import HCSR04
from lib.micropyGPS import MicropyGPS
import machine as m
import dht


ubidotsToken = "BBUS-09DidGsAEKGqkJ7U76nm3btnWFjgHP"

my_gps = MicropyGPS()
gps_serial = m.UART(2, baudrate=9600, tx=17, rx=16)

def convert_to_decimal(degrees, direction):
    decimal = degrees[0] + (degrees[1] / 60)
    if direction in ('S', 'W'):
        decimal = -decimal
    return decimal

def led_cb(topic, msg):
    # print(msg)
    # if msg.decode() == '1.0':
    #     led.value(1)
    # else:
    #     led.value(0)
    print((topic, msg))
    if topic == b'notification' and msg == b'received':
        print('ESP received hello message')

clientID = "esp32wroom32"
sensorDht = dht.DHT22(m.Pin(15))
sensorUltraSonic = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)
led = m.Pin(27, m.Pin.OUT)
client = MQTTClient("clientID", "industrial.api.ubidots.com", 1883, user = ubidotsToken, password = ubidotsToken)
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

pin13 = m.Pin(13, m.Pin.IN, m.Pin.PULL_UP)

def publish():
    
    while True:
        try:
            while gps_serial.any():
                data = gps_serial.read()
                
                for byte in data:
                    status = my_gps.update(chr(byte))
                    if status is not None:
                        lat = convert_to_decimal(my_gps.latitude, my_gps.latitude[2])
                        lon = convert_to_decimal(my_gps.longitude, my_gps.longitude[2])
                        var = repr(pin13.value())
                        
                        msg = b'{"location": {"value":%s, "context":{"lat":%s, "lng":%s}}}' % (var, lat, lon)
                        
                        client.publish(b"/v1.6/devices/ESP32_THSS", msg)
                    
                        print('UTC Timestamp:', my_gps.timestamp)
                        print('Date:', my_gps.date_string('long'))
                        print(f"Latitude: {lat:.6f}, Longitude: {lon:.6f}")
                        print('Altitude:', my_gps.altitude)
                        print('Satellites in use:', my_gps.satellites_in_use)
                        print('Horizontal Dilution of Precision:', my_gps.hdop)
                        print()
                
        except Exception as e:
            print(f"An error occurred: {e}")
            

        print("woalah gtu")
        checkwifi()

        # sensorDht.measure()
        # temp = sensorDht.temperature()
        # hum = sensorDht.humidity()
        # temp_f = temp * (9/5) + 32.0
        # distance = sensorUltraSonic.distance_cm()
        # print('Temperature: %3.1f C' %temp)
        # print('Temperature: %3.1f F' %temp_f)
        # print('Humidity: %3.1f %%' %hum)
        # print('Distance:', distance, 'cm')
        # if gps_serial.any():
        #    line = gps_serial.readline()  # Read a complete line from the UART
        # if line:
        #     line = line.decode('utf-8')
        #     print(line.strip())
        # sleep(0.5)
        # msg = b'{"location": {"value":%s, "context":{"lat":%s, "lng":%s}}}' % (var, lat, lng)
        
        # msg = b'{"temperature": {"value":%s}, "humidity": {"value":%s}, "distance": {"value":%s}}' % (temp, hum, distance)
        # #print(msg)
        # print("test publish..")
        # client.publish(b"/v1.6/devices/ESP32_THSS", msg)
        client.check_msg()

        sleep(2)

# def subscribe():
#     client.set_callback(led_cb)
#     client.subscribe(b"/v1.6/devices/esp32_thss/led")

#     while True:
#         client.check_msg()
#         sleep(2)
    
    
publish()   
# subscribe()