from motor import Motor
from encoder import Encoder

class Overspeed:
    def __init__(self, motor: Motor, encoder: Encoder, desiredVel: int):
        self.motor = motor
        self.encoder = encoder
        self.desiredVel = desiredVel
    
    def setDesiredVel(self, vel: int):
        self.desiredVel = desiredVel
    
    def followVelocity(self):
        if (self.encoder.getVelocity() >= self.desiredVel):
            self.motor.forward(0)
        else:
            self.motor.forward(1)

