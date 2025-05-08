import pigpio
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
import time

class turntable:
    def __init__(self):
        self.gpio = pigpio.pi()
        self.factory = PiGPIOFactory()

        self.debug = False

        self.solenoidFireTime = 0.5
        self.elevatorRunTime = 1.06 #Super inconsistent

        self.bluePin = 23 # Setup all pins
        self.redPin = 27
        self.whitePin = 17
        self.elevatorMC1 = 24
        self.elevatorMC2 = 25
        self.tableServoPin = 4

        self.outPins = [self.bluePin, self.redPin, self.whitePin, self.tableServoPin, self.elevatorMC1, self.elevatorMC2]
        for pin in self.outPins:
            self.gpio.set_mode(pin,pigpio.OUTPUT)
            self.gpio.write(pin,0)

        self.tableServo = AngularServo(self.tableServoPin, min_pulse_width=0.0006, max_pulse_width=0.0023, pin_factory=self.factory)
        self.tableServo.angle = None

    def unpowerPins(self):
        for pin in self.outPins:
            self.gpio.write(pin,0)

    def debugMode(self):
        print("Debug Mode")
        self.debug = True

    def elevatorDump(self):
        self.gpio.write(self.elevatorMC1, 0) #Up
        self.gpio.write(self.elevatorMC2, 1)
        time.sleep(self.elevatorRunTime)

        self.gpio.write(self.elevatorMC1, 0) #Stop
        self.gpio.write(self.elevatorMC2, 0)
        time.sleep(0.5)

        self.gpio.write(self.elevatorMC1, 1) #Down
        self.gpio.write(self.elevatorMC2, 0)
        time.sleep(self.elevatorRunTime) #Why

        self.gpio.write(self.elevatorMC1, 0) #Stop
        self.gpio.write(self.elevatorMC2, 0)

    def dispenseMarble(self, color, player): #color: blue, white, or red | player: P1, P2, B
        if player == "P1":
            self.tableServo.angle = 90
        elif player == "B":
            self.tableServo.angle = 10
        elif player == "P2":
            self.tableServo.angle = -80

        if not self.debug:
            if color == "blue":
                self.gpio.write(self.bluePin, 1)
                time.sleep(self.solenoidFireTime)
                self.gpio.write(self.bluePin, 0)
            elif color == "red":
                self.gpio.write(self.redPin, 1)
                time.sleep(self.solenoidFireTime)
                self.gpio.write(self.redPin, 0)
            elif color == "white":
                self.gpio.write(self.whitePin, 1)
                time.sleep(self.solenoidFireTime)
                self.gpio.write(self.whitePin, 0)

        time.sleep(1.25)
        self.elevatorDump()
        time.sleep(0.2)
        self.tableServo.angle = 0
        time.sleep(0.4)

if __name__ == "__main__":
    import turntable
    import sorter
    from multiprocessing import Process
    def startSorter():
        s = sorter.sorter()
        s.sorterLoop()

    try:
        d = turntable.turntable()
        #d.debugMode()

        sProc = Process(target=startSorter)
        sProc.start()

        print("Dispensing red to B")
        while True:
            d.dispenseMarble("blue", "P1")
            time.sleep(2)
            d.dispenseMarble("red", "P2")
            time.sleep(2)
            d.dispenseMarble("white", "P1")
            time.sleep(2)
    except KeyboardInterrupt:
        print("Quitting...")
        d.unpowerPins()
