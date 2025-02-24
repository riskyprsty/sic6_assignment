import time

import network

import machine as m

sta_if = network.WLAN(network.STA_IF); sta_if.active(True)

sta_if.scan() 

sta_if.connect("TP-Link_AD7C", "88515762")

sta_if.isconnected()

time.sleep(3)