import RPi.GPIO as GPIO

class Motor:
    def __init__(self, in1: int, in2: int, en: int, polarity: bool):
        self.in1 = in1
        self.in2 = in2
        self.polarity = polarity

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(in1,GPIO.OUT)
        GPIO.setup(in2,GPIO.OUT)
        GPIO.setup(en,GPIO.OUT)
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)

        self.p=GPIO.PWM(en,1000)
        self.p.start(0)
    
    def forward(self, power: float):
        adjPower = power * 100

        if (not self.polarity):
            GPIO.output(self.in1,GPIO.HIGH)
            GPIO.output(self.in2,GPIO.LOW)
        else:
            GPIO.output(self.in1,GPIO.LOW)
            GPIO.output(self.in2,GPIO.HIGH)
        self.p.ChangeDutyCycle(adjPower)

    def backward(self, power: float):
        self.polarity = not self.polarity

        self.forward(power)

        self.polarity = not self.polarity