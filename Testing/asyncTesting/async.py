import time
import asyncio
import threading

i=0

def counter():
    global i
    while True:
        i += 1
        if i>1000:
            i=0

thread = threading.Thread(target=asyncio.run, args=(counter(),))
thread.start()

while True:
    print(i)
