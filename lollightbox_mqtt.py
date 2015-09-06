#!/usr/bin/python2

###
# Copyright 2015, Aurel Wildfellner.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

import time
import serial
import argparse

import mosquitto

import sys
import time
from neopixel import *

# LED strip configuration:
LED_COUNT      = 5      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

color =  [16711680, 16728064, 16744448, 16760576, 16776960, 12582656, 8453888, 4259584, 65280, 65334, 65408, 65471, 65535, 49151, 33023, 16639, 255, 4194559, 8388863, 12517631, 16711935, 16711871, 16711808, 16711744, 8684676, 16777215]
strip = None


def scale(percentage, min, max):
    return percentage * (max - min) / 100 + min;


class MQTT_TOPICS:
   lightbox  = "devlol/h19/colorTest"



def on_message(client, msg):
    global strip
    #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    print msg.payload
    print round(scale(int(msg.payload), 0, 25),0)

    for i in range(LED_COUNT):
        strip.setPixelColor(i,color[int(round(scale(int(msg.payload), 0, 25),0))])
    strip.show()
    time.sleep(50/1000.0)


def on_disconnect(client):
    connected = False
    while not connected:
        try:
            client.reconnect()
            connected = True
            # resubscribe to the topics
            client.subscribe(MQTT_TOPICS.lightbox)
        except:
            print("Failed to reconnect...")
            time.sleep(1)


def main():
    global strip

    ## Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="192.168.8.2")

    args = parser.parse_args() 
    brokerHost = args.host

    ## setup neo pixel strip
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()
    
    
    ## setup MQTT client
    client = mosquitto.Mosquitto("devlollightbox_h19")
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.user_data = strip

    try:
        client.connect(brokerHost)
    except:
        print("failed to connect")
        on_disconnect(client, None, None)

    print("connected to brokber")
    ## subscribe to topics
    client.subscribe(MQTT_TOPICS.lightbox)

    ## winkekatze
    while True:
        client.loop()


if __name__ == "__main__":
    main()

