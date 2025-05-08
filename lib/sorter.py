import pigpio
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
import time
import read_PWM

class sorter:
    def __init__(self): #This is kinda cool but OOP sucks
        self.gpio = pigpio.pi()
        self.factory = PiGPIOFactory() #I have no idea what this is but it makes the servo less jittery

        self.debug = False 

        self.solPin = 22
        self.sortServoPin = 16
        self.colorOUTPin = 5
        self.colorS3Pin = 6

        self.solenoidFireTime = 0.4 #seconds
        self.scanTime = 5/1000 #ms
        self.confirmThreshold = 200/(self.scanTime*1000)

        self.outPins = [self.solPin, self.sortServoPin, self.colorOUTPin, self.colorS3Pin]
        for pin in self.outPins: #Init Pins
            self.gpio.set_mode(pin, pigpio.OUTPUT)
            self.gpio.write(pin, 0) #Just in case one of them turns on for whatever reason

        self.sortServo = AngularServo(self.sortServoPin, min_pulse_width=0.0006, max_pulse_width=0.0023, pin_factory=self.factory)
        self.sortServo.angle = None

    def unpowerPins(self):
        for pin in self.outPins:
            self.gpio.write(pin,0)

    def debugMode(self):
        print("Debug Mode") #Debug Mode!
        self.debug = True

    def sortMarble(self, color): #Move track to correct marble pos
        if color == "blue":
            self.sortServo.angle = 90
        elif color == "red":
            self.sortServo.angle = 0
        elif color == "white":
            self.sortServo.angle = -90

        time.sleep(0.1)

        if color != "none":
            self.gpio.write(self.solPin, 1)
            time.sleep(self.solenoidFireTime)
            self.gpio.write(self.solPin, 0)

    def calibrateSensor(self, scanTime, colorOUT):
        self.sortServo.angle = 90
        self.gpio.write(self.solPin, 1) # Clear if there is a marble in there
        time.sleep(self.solenoidFireTime)
        self.gpio.write(self.solPin, 0)

        time.sleep(1) #Have to wait for the sensor to 'warm up'
        self.sortServo.angle = -90
        self.gpio.write(self.colorS3Pin, 1)
        time.sleep(scanTime)
        blueAmbient = colorOUT.frequency()

        self.gpio.write(self.colorS3Pin, 0)
        time.sleep(scanTime)
        redAmbient = colorOUT.frequency()

        if self.debug:
            print("Blue Cal:",blueAmbient)
            print("Red Cal:",redAmbient)

        return redAmbient, blueAmbient

    def pollColor(self, scanTime, colorOUT, redAmbient, blueAmbient):
        self.gpio.write(self.colorS3Pin, 1)
        time.sleep(scanTime)
        blueFreq = colorOUT.frequency()

        self.gpio.write(self.colorS3Pin, 0)
        time.sleep(scanTime)
        redFreq = colorOUT.frequency()

        #Map the freq to a range of 0-100
        blueColor = self.map_range(blueFreq, blueAmbient+700, blueAmbient, 100, 0) 
        redColor = self.map_range(redFreq, redAmbient+700, redAmbient, 100, 0)

        if self.debug:
            print("Blue:",blueFreq,"Red:",redFreq)

        #Determine what color it is based on the values
        if blueColor > 200 and redColor > 200:
            return "white"
        elif blueColor > 100:
            if blueColor < redColor: #why do i have to do this
                return "red"
            else:
                return "blue"
        elif redColor > 100:
            return "red"
        else:
            return "none"

    def sorterLoop(self):
        colorOUT = read_PWM.reader(self.gpio, self.colorOUTPin)
        redAmbient, blueAmbient = self.calibrateSensor(self.scanTime, colorOUT)
        confirms = 0

        while True:
            color = self.pollColor(self.scanTime, colorOUT, redAmbient, blueAmbient)

            if color == "none":
                confirms = 0
            else:
                confirms += 1

            if self.debug:
                print(color, confirms)

            if confirms >= self.confirmThreshold:
                self.sortMarble(color)
                confirms = 0

    def map_range(self, x, in_min, in_max, out_min, out_max): #Yup
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

if __name__ == "__main__":
    import sorter

    try:
        s = sorter.sorter()
        s.debugMode()
        s.sorterLoop()
    except KeyboardInterrupt:
        print("Quitting...")
        s.unpowerPins()
