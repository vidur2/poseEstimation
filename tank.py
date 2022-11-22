from scipy.interpolate import splev
from math import e
from motor import Motor
from encoder import Encoder
from controller import Overspeed
import sys

sys.path.append("../AprilTag/scripts")

import apriltag_video

with open("./y_x.pickle", 'rb') as f:
    path = loads(codecs.decode(f.read(), "base64"))

with open("./t_x.pickle", 'rb') as f:
    tX = loads(codecs.decode(f.read(), "base64"))

with open("./x_t.pickle", 'rb') as f:
    xT = loads(codecs.decode(f.read(), "base64"))

path = None
maxPowah = 1

def curvature(currX):
    yDoublePrime = splev(currX, path["diff2"])
    yPrime = splev(currX, path["diff"])

    return yDoublePrime/((1+(yPrime)**2)**(3/2))

def transform(kappa):
    return e**(-kappa) * maxPowah

def adjPower(curvature, currX):
    direc = getDirection(currX)
    if (curvature >= 0 and direc >= 0 or curvature < 0 and direc < 0 ):
        return (maxPowah, transform(curvature))
    else:
        return (transform(abs(curvature)), maxPowah)

def getDirection(currX):
    currT = splev(currX, tck=tX["self"])
    currVel = splev(currT, tck=xT["diff"])

    return currVel


def getPower(currX):
    kappa = curvature(currX)
    return adjPower(kappa, currX)

def main():
    lastPose = path["lastPose"]
    lMotor = Motor(16, 25, 12, False)
    rMotor = Motor(5, 6, 13, True)

    rEncoder = Encoder(4)
    lEncoder = Encoder(26)

    rController = Overspeed(rMotor, rEncoder, 0, 1, .25)
    lController = Overspeed(lMotor, lEncoder, 0, .7)

    
    for pos in apriltag_video.apriltag_video([0]):
        if (len(pos)):
            yVal = pose[2][3]/5.2
            xVal = pose[0][3]

            if (abs(lastPose - xVal) < 0.1 and abs(lastPose - yVal) < 0.1):
                break
            
            rPower, lPower = getPower(xVal)
            rRatio = rPower * 50
            lPower = lPower * 50
            
            rController.setDesiredVel(rRatio)
            lController.setDesiredVel(lRatio)
            
            # Maybe continue velocity if unseen?
            lController.followVelocity()
            rController.followVelocity()
        else:
            lMotor.forward(0)
            rMotor.forward(0)
    lMotor.forward(0)
    rMotor.forward(0)


if (__name__== "__main__"):
    main()