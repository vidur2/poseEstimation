from motor import Motor
from time import sleep, time
from encoder import Encoder


def test():
    lMotor = Motor(16, 25, 12, False)
    rMotor = Motor(5, 6, 13, True)

    rEncoder = Encoder(4)
    lEncoder = Encoder(17)

    lMotor.forward(0.25)
    rMotor.forward(0.25)
    startTime = time()

    while (time - startTime < 2):
        print(rEncoder.getVelocity())
        print(lEncoder.getVelocity())
    rMotor.forward(0)
    lMotor.forward(0)

def velTest():
    pass

if __name__ == '__main__':
    test()