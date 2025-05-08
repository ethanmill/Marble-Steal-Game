import pigpio
from time import sleep
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

gpio = pigpio.pi()
factory = PiGPIOFactory()

servoPin = 4
servo = AngularServo(servoPin, min_pulse_width=0.0006,max_pulse_width=0.0023, pin_factory=factory)

while True:
    try :
        servo.angle = 90
        sleep(1)
        servo.angle = 0
        sleep(1)
        servo.angle = -90
        sleep(1)

    except KeyboardInterrupt:
        print("Stopping...")
        gpio.cleanup()
        exit()
