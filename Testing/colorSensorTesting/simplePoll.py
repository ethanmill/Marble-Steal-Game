import RPi.GPIO as gpio
import time

signal = 6

def setup():
    gpio.setmode(gpio.BCM)
    gpio.setup(signal, gpio.IN)

setup()
while(1):
    print(gpio.input(signal))
