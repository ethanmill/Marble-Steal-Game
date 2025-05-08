import pigpio
import time

class pBuzzer:
    def __init__(self):
        self.gpio = pigpio.pi()

        self.debug = False 

        self.buzzerPin = 18 #Has to be a pin capable of PWM

        self.dutyCycle = 50*10000 #Volume in a way but hnah

    def playFreq(self, freq, noteTime, fullTime): # Freq in Hz, time in sec
        self.gpio.hardware_PWM(self.buzzerPin, freq, self.dutyCycle)
        time.sleep(noteTime)
        self.stop()
        time.sleep(fullTime)

    def stop(self):
        self.gpio.hardware_PWM(self.buzzerPin, 0, 0)

    def wrongGuess(self):
        self.playFreq(200, 0.7, 0)
        self.playFreq(100, 0.7, 0)

    def rightGuess(self):
        self.playFreq(400, 0.25, 0)
        self.playFreq(800, 0.25, 0)

    def useItem(self):
        self.playFreq(400,0.2, 0.2)

    def song(self, bpm):
        quarter = 60/bpm
        self.playFreq(82, quarter/4, 0.05)
        self.playFreq(82, quarter/4, 0.05)
        self.playFreq(164, quarter/4, 0.05)
        self.playFreq(82, quarter/4, 0.05)
        self.playFreq(82, quarter/4, 0.05)
        self.playFreq(154, quarter/4, 0.05)
        self.playFreq(82, quarter/4, 0.05)
        self.playFreq(82, quarter/4, 0.05)
        self.playFreq(146, quarter, 0.05)
        self.playFreq(138, quarter, 0.05)
        self.playFreq(130, quarter*2, 0.05)
        self.playFreq(82, quarter/4, 0.05)
        self.playFreq(82, quarter/4, 0.05)
        self.playFreq(123, quarter/4, 0.05)
        self.playFreq(82, quarter/4, 0.05)
        self.playFreq(82, quarter/4, 0.05)
        self.playFreq(116, quarter/4, 0.05)
        self.playFreq(82, quarter/4, 0.05)
        self.playFreq(82, quarter/4, 0.05)
        self.playFreq(110, quarter/4, 0.05)
        self.playFreq(82, quarter/4, 0.05)
        self.playFreq(103, quarter/4, 0.05)
        self.playFreq(82, quarter/4, 0.05)
        self.playFreq(98, quarter/4, 0.05)
        self.playFreq(82, quarter/4, 0.05)
        self.playFreq(92, quarter/4, 0.05)
        self.playFreq(87, quarter/4, 0.05)

if __name__ == "__main__":
    import sound

    try:
        b = sound.pBuzzer()
        b.wrongGuess()
        time.sleep(0.5)
        b.rightGuess()
        time.sleep(0.5)
        b.useItem()
    except KeyboardInterrupt:
        print("Ctrl+C Quitting...")
        b.stop()
