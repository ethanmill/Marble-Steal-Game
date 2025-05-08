import pigpio
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
import time
import read_PWM

gpio = pigpio.pi()
factory = PiGPIOFactory()

Debug = False 

# All Pins
s1Pin = 22
s2Pin = 27
s3Pin = 17
s4Pin = 23
sortServoPin = 16
tableServoPin = 4
colorS3Pin = 6
colorOUTPin = 5
elevatorMC1 = 24
elevatorMC2 = 25

outPins = [s1Pin, s2Pin, s3Pin, s4Pin, sortServoPin, tableServoPin, colorS3Pin, elevatorMC1, elevatorMC2]
for pin in outPins:
    print(pin,"OUT")
    gpio.set_mode(pin, pigpio.OUTPUT)
    gpio.write(pin, 0)

sortServo = AngularServo(sortServoPin, min_pulse_width=0.0006,max_pulse_width=0.0023, pin_factory=factory)
sortServo.angle = None
tableServo = AngularServo(tableServoPin, min_pulse_width=0.0006,max_pulse_width=0.0023, pin_factory=factory)
tableServo.angle = None

solenoidFireTime = 0.3 #seconds
elevatorRunTime = 1.19
scanTime = 5/1000
confirmThreshold = 200/(scanTime*1000)
color = "none"

redFreq = 0
redColor = 0
blueFreq = 0
blueColor = 0
confirms = 0
timer = 0

stable = False

def elevatorUp():
    gpio.write(elevatorMC1, 0);
    gpio.write(elevatorMC2, 1);

def elevatorDown():
    gpio.write(elevatorMC1, 1);
    gpio.write(elevatorMC2, 0);

def elevatorStop():
    gpio.write(elevatorMC1, 0);
    gpio.write(elevatorMC2, 0);

def dispenseMarble(color, player):
    print("Dispensing:",color)
    if color == "blue":
        pin = s4Pin
    elif color == "red":
        pin = s2Pin
    elif color == "white":
        pin = s3Pin

    if player == "P1":
        tableServo.angle = -90
    elif player == "B":
        tableServo.angle = 0
    elif player == "P2":
        tableServo.angle = 90

    if isinstance(pin,int):
        gpio.write(pin, 1)
        time.sleep(solenoidFireTime)
        gpio.write(pin, 0)

    time.sleep(1)
    elevatorUp()
    time.sleep(elevatorRunTime+0.2)
    elevatorStop()
    time.sleep(0.5)
    elevatorDown()
    time.sleep(elevatorRunTime)
    elevatorStop()

def sortMarble(color):
    print("Sorting:", color)
    if color == "blue":
        sortServo.angle = 90
    elif color == "red":
        sortServo.angle = 0
    elif color == "white":
        sortServo.angle = -90

    time.sleep(0.5)

    if color != "none":
        gpio.write(s1Pin, 1)
        time.sleep(solenoidFireTime)
        gpio.write(s1Pin, 0)

def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def pollColor(scanTime):
    global Debug
    gpio.write(colorS3Pin, 1)
    time.sleep(scanTime)
    blueFreq = colorOUT.frequency()

    gpio.write(colorS3Pin, 0)
    time.sleep(scanTime)
    redFreq = colorOUT.frequency()

    blueColor = map_range(blueFreq, blueAmbient+1200, blueAmbient, 100, 0)
    redColor = map_range(redFreq, redAmbient+800, redAmbient, 100, 0)
    if Debug:
        print("Blue:",round(blueFreq-blueAmbient, 2),"Red",round(redFreq-redAmbient, 2))
        print("Blue:",blueColor,"Red",redColor)

    if blueColor > 200 and redColor > 200:
        return "white"
    elif blueColor > 100:
        if blueColor < redColor: #why
            return "red"
        else:
            return "blue"
    elif redColor > 100:
        return "red"
    else:
        return "none"

def calibrateSensor(scanTime):
    print("Calibrating...")
    time.sleep(2) #Wait for color sensor to warm up
    gpio.write(colorS3Pin, 1)
    time.sleep(scanTime)
    blueAmbient = colorOUT.frequency()
    print("Blue Ambient:",blueAmbient)

    gpio.write(colorS3Pin, 0)
    time.sleep(scanTime)
    redAmbient = colorOUT.frequency()
    print("Red Ambient:",redAmbient)

    time.sleep(1)

    return redAmbient, blueAmbient

colorOUT = read_PWM.reader(gpio, colorOUTPin)

if __name__ == "__main__":
    
    redAmbient, blueAmbient = calibrateSensor(scanTime)

    while True:
        try:
            timer += 1
            color = pollColor(scanTime)
            if not Debug:
                print(color,confirms,timer)
    
            if color == "none":
                confirms = 0
            else:
                confirms += 1
    
            if confirms >= confirmThreshold and not Debug:
                sortMarble(color)
                confirms = 0
    
            if timer == 200:
                dispenseMarble("red", "P1")
            elif timer == 400:
                dispenseMarble("white", "P2")
            elif timer >= 600:
                dispenseMarble("blue", "B")
                timer = 0
    
        except KeyboardInterrupt:
            print("Unpowering")
            for pin in outPins:
                gpio.output(pin, 0)
    
            exit()
