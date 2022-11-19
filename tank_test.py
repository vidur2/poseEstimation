from motor import Motor
from time import sleep


def test():
    lMotor = Motor(16, 25, 12, False)
    rMotor = Motor(5, 6, 13, True)

    lMotor.forward(lPower)
    rMotor.forward(rPower)
    sleep(2)
    rMotor.forward(0)
    lMotor.forward(0)