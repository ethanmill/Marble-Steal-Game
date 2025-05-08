import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

s1Pin = 17
s2Pin = 27
s3Pin = 22
s4Pin = 23

pins = [s1Pin, s2Pin, s3Pin, s4Pin]

gpio.setup(s1Pin, gpio.OUT)
for pin in pins:
    print(pin)
    gpio.setup(pin, gpio.OUT)

i=0

while True:
    try:
        time.sleep(1)
        print(i)
        for index,sol in enumerate(pins):
            if index == i:
                gpio.output(sol, 1)
            else:
                gpio.output(sol, 0)
        i += 1
        if i >= len(pins):
            i = 0
    except KeyboardInterrupt:
        print("Unpowering")
        for pin in pins:
            gpio.output(pin, 0)

        exit()
