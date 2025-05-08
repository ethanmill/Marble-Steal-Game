import pigpio
import read_PWM
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

gpio = pigpio.pi()

scanTime = 10/1000 #milliSeconds
confirmThreshold = 200/(scanTime*1000)

detectedColor = "none" #none, white, blue, red

pulseCount = 0

redFreq = 0
blueFreq = 0

redColor= 0
blueColor= 0

confirms = 0
stable = False

gpio.set_mode(s3, pigpio.OUTPUT)
p = read_PWM.reader(gpio, out)

def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

while True:
    try:
        gpio.write(s3, 0) #read blue
        time.sleep(scanTime)
        blueFreq = p.frequency()
        blueColor = map_range(blueFreq, 1400, 1500, 100, 0)

        gpio.write(s3, 1) #read red
        time.sleep(scanTime)
        redFreq = p.frequency()
        redColor = map_range(redFreq, 1550, 1700, 100, 0)

        if blueColor < -400 and redColor < -400:
            color = "white"
            confirms += 1
        elif blueColor > 100:
            color = "blue"
            confirms += 1
        elif redColor > 100:
            color = "red"
            confirms += 1
        else:
            color = "none"
            confirms = 0

        if confirms >= confirmThreshold:
            stable = True
            confirms = confirmThreshold
        else:
            stable = False

        print("Red:", round(redFreq,1), "Blue:", round(blueFreq,1), "Color:", color, stable)
        #print("Red:", round(redColor,1), "Blue:", round(blueColor,1), "Color:", color, stable)

    except KeyboardInterrupt:
        exit()
