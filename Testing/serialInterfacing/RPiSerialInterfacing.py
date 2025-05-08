import serial
import pigpio
import time
from threading import Thread

ser = serial.Serial("/dev/ttyACM0", 9600)
ser.baudrate = 9600
cmdQueue = []

def pollSerial(threadname):
    while True:
        global cmdQueue
        recieved = ser.readline() 
        cmdQueue.append(str(recieved)[2:-5])

def printThing(text, times):
    for i in range(times):
        print(text)

if __name__ == "__main__":
    serialThread = Thread(target=pollSerial, args=("Serial Poll",))
    serialThread.start()
    while True:
        try:
            if len(cmdQueue) != 0:
                #cmd, args = cmdQueue[0].split(" ",1) #I think you can do this?
                cmd = cmdQueue[0].split(" ",1)[0]
                args = cmdQueue[0].split(" ",1)[1]

                if cmd == "printThing":
                    arg = args.split()
                    printThing(str(arg[0]), int(arg[1]))
                    cmdQueue.pop(0)

        except KeyboardInterrupt:
            print("Done")
            quit()
