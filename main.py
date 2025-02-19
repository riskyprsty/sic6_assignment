from umqtt.robust import MQTTClient

import machine as m

ubidotsToken = "BBUS-I93MQuistalSIcgLgFQGJ1fq19C79jVeha1BD2RYWjaxAGThqinIwqJ"

clientID = "esp32wroom32"

client = MQTTClient("clientID", "industrial.api.ubidots.com", 1883, user = ubidotsToken, password = ubidotsToken)

def checkwifi():

    while not sta_if.isconnected():

        time.sleep_ms(500)

        print(".")

        sta_if.connect()

pin13 = m.Pin(13, m.Pin.IN, m.Pin.PULL_UP)

def publish():

    while True:

        checkwifi()

        client.connect()

        lat = -7.280389

        lng = 112.7867191

        var = repr(pin13.value())

        msg = b'{"location": {"value":%s, "context":{"lat":%s, "lng":%s}}}' % (var, lat, lng)

        print(msg)

        client.publish(b"/v1.6/devices/ESP32_THSS", msg)

        time.sleep(20)

publish()