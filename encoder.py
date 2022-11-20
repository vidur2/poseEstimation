import time
import RPi.GPIO as GPIO

class Encoder:
    def __init__(self, port):
        self.secsBetweenTicks = 0
        self.position = 0

        self.prevTime = time.time()
        
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(port, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(port, GPIO.FALLING, callback=self.resetVelocity)
        PIO.add_event_detect(port, GPIO.RISING, callback=self.setVelocity)

    def setVelocity(self):
        self.position += 1
        if (self.position % 8 == 0):
            self.velocity = time.time() - self.prevTime

    def resetVelocity(self):
        self.prevTime = time.time()

    def getVelocity(self):
        return 1/self.secsBetweenTicks * (self.secsBetweenTicks != 0)
    
    def getPosition(self):
        return self.position