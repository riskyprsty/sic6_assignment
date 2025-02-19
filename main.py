from umqtt.robust import MQTTClient
from time import sleep, sleep_ms
import machine as m
import dht

ubidotsToken = "BBUS-09DidGsAEKGqkJ7U76nm3btnWFjgHP"

# gps_serial = m.UART(2, baudrate=9600, tx=35, rx=32)

clientID = "esp32wroom32"
sensorDht = dht.DHT22(m.Pin(15))
sensorUltraSonic = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)
client = MQTTClient("clientID", "industrial.api.ubidots.com", 1883, user = ubidotsToken, password = ubidotsToken)

def checkwifi():

    while not sta_if.isconnected():

        sleep_ms(500)

        print(".")

        sta_if.connect()

pin13 = m.Pin(13, m.Pin.IN, m.Pin.PULL_UP)

def publish():

    while True:

        checkwifi()

        client.connect()
        sensorDht.measure()
        temp = sensorDht.temperature()
        hum = sensorDht.humidity()
        temp_f = temp * (9/5) + 32.0
        distance = sensorUltraSonic.distance_cm()
        print('Temperature: %3.1f C' %temp)
        print('Temperature: %3.1f F' %temp_f)
        print('Humidity: %3.1f %%' %hum)
        print('Distance:', distance, 'cm')
        # if gps_serial.any():
        #    line = gps_serial.readline()  # Read a complete line from the UART
        # if line:
        #     line = line.decode('utf-8')
        #     print(line.strip())
        # sleep(0.5)
        # msg = b'{"location": {"value":%s, "context":{"lat":%s, "lng":%s}}}' % (var, lat, lng)
        msg = b'{"temperature": {"value":%s}, "humidity": {"value":%s}, "distance": {"value":%s}}' % (temp, hum, distance)
        print(msg)

        client.publish(b"/v1.6/devices/ESP32_THSS", msg)

        sleep(20)

publish()