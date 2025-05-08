import time
from threading import Thread
a = 0

def thread2(threadname):
    global a 
    while True:
        a += 1
        time.sleep(1)

def thread1(threadname):
    while a<10:
        print(a)

thread1 = Thread(target=thread1, args=("Thread-1",))
thread2 = Thread(target=thread2, args=("Thread-2",))

thread1.start()
thread2.start()

thread1.join()
thread2.join()
