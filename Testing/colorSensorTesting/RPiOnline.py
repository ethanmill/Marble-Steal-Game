import RPi.GPIO as GPIO
import time

s3 = 5
signal = 6
NUM_CYCLES = 10

def setup():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(signal,GPIO.IN)
  GPIO.setup(s3,GPIO.OUT)
  print("\n")

def loop():
  temp = 1
  while(1):  

    GPIO.output(s3,GPIO.LOW)
    time.sleep(0.1)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start      #seconds to run for loop
    red  = NUM_CYCLES / duration   #in Hz

    GPIO.output(s3,GPIO.HIGH)
    time.sleep(0.1)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start
    blue = NUM_CYCLES / duration
    print("red value - ", red, " blue value - ",blue)

def endprogram():
    GPIO.cleanup()

if __name__=='__main__':
    
    setup()

    try:
        loop()

    except KeyboardInterrupt:
        gpio.cleanup()
        endprogram()
