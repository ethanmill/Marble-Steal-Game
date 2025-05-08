import pigpio
import time 

gpio = pigpio.pi()

elevatorPow = 12
elevatorMC1 = 24
elevatorMC2 = 25

outPins = [elevatorMC1, elevatorMC2]
for pin in outPins:
    gpio.set_mode(pin, pigpio.OUTPUT)
    gpio.write(pin, 0)

def elevatorUp(rate):
    gpio.write(elevatorMC1, 1)
    gpio.write(elevatorMC2, 0)
    gpio.set_PWM_dutycycle(elevatorPow, 255)

def elevatorDown(rate):
    gpio.write(elevatorMC1, 0)
    gpio.write(elevatorMC2, 1)
    gpio.set_PWM_dutycycle(elevatorPow, 255)

def elevatorStop():
    gpio.write(elevatorMC1, 0)
    gpio.write(elevatorMC2, 0)
    gpio.set_PWM_dutycycle(elevatorPow, 0)

while True:
    elevatorUp(1)
    print("Up")
    time.sleep(2)
    elevatorDown(1)
    print("Down")
    time.sleep(2)
    elevatorStop()
    print("Stop")
    time.sleep(2)
