import time

import network

import machine as m

sta_if = network.WLAN(network.STA_IF); sta_if.active(True)

sta_if.scan() 

sta_if.connect("tehyung_oppa", "39267207")

sta_if.isconnected()

time.sleep(3)