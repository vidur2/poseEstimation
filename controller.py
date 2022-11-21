from motor import Motor
from encoder import Encoder

class Overspeed:
    def __init__(self, motor: Motor, encoder: Encoder, desiredVel: int, maxPow: int=1, minPow: int=0):
        self.motor = motor
        self.encoder = encoder
        self.desiredVel = desiredVel
        self.maxPow = maxPow
        self.minPow = minPow
    
    def setDesiredVel(self, vel: int):
        self.desiredVel = desiredVel
    
    def followVelocity(self):
        if (self.encoder.getVelocity() >= self.desiredVel):
            self.motor.forward(self.minPow)
        else:
            self.motor.forward(self.maxPow)

