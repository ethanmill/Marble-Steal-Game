import RPi.GPIO as gpio
import time

out = 13
s3 = 6
# !!! -------------------------------------------------- !!!
# 
# To ground: gnd, s1, s2, 
# 
# To 5v: Vcc, 
# 
# Scale S0 S1
# 0%    0  0 (Off)
# 2%    0  1 <--- this is 10-12kHz
# 20%   1  0
# 100%  1  1
# 
# !!! -

scanTime = 1 #Seconds
confirmThreshold = 100

detectedColor = "none" #none, white, blue, red

pulseCount = 0

redFreq = 0
blueFreq = 0
reenFreq = 0

confirms = 0

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

gpio.setup(s3, gpio.OUT)
gpio.setup(out, gpio.IN)

def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

while True:
    try:
        gpio.output(s3, 0) #read red

        start = time.time()
        pulseCount = 0
        while time.time()-start < scanTime:
            if gpio.input(out) == 0:
                pulseCount += 1
        redFreq = pulseCount
        redColor = map_range(redFreq, 1375, 2300, 100, 0)

        gpio.output(s3, 1) #read blue
        time.sleep(0.1)

        start = time.time()
        pulseCount = 0
        while time.time()-start < scanTime:
            if gpio.input(out) == 0:
                pulseCount += 1
        redFreq = pulseCount
        redColor = map_range(redFreq, 1375, 2300, 100, 0)

        print("Red: "+str(round(redFreq,5))+" Blue: "+str(round(blueFreq,5)))
        time.sleep(0.1)
    except KeyboardInterrupt:
        gpio.cleanup()
        exit()
