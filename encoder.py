import time
import RPi.GPIO as GPIO

class Encoder:
    def __init__(self, port):
        self.secsBetweenTicks = 0
        self.position = 0

        self.prevTime = time.time()
        
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(port, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(port, GPIO.FALLING, callback=self.setVelocity)
        # GPIO.add_event_detect(port, GPIO.RISING, callback=self.setVelocity)

    def setVelocity(self, channel):
        self.position += 1
        if (self.position % 8 == 0):
            self.secsBetweenTicks = time.time() - self.prevTime
            self.resetVelocity()

    def resetVelocity(self):
        self.prevTime = time.time()

    def getVelocity(self):
        if (self.secsBetweenTicks != 0 and time.time() - self.prevTime < .25):
            return (1/self.secsBetweenTicks)
        else:
            return 0
    
    def getPosition(self):
        return self.position