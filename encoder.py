import time
import RPi.GPIO as GPIO

class Encoder:
    def __init__(self, port):
        self.velocity = 0
        self.position = 0

        self.prevTime = time.time()
        
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(port, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(port, GPIO.FALLING, callback=self.resetVelocity)
        PIO.add_event_detect(port, GPIO.RISING, callback=self.setVelocity)

    def setVelocity(self):
        self.position += 1
        self.velocity = 1/(time.time() - self.prevTime)

    def resetVelocity(self):
        self.prevTime = time.time()

    def getVelocity(self):
        return self.velocity
    
    def getPosition(self):
        return self.position