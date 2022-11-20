from scipy.interpolate import splev
from math import e
from motor import Motor
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
    for pos in apriltag_video.apriltag_video([0]):
        yVal = pose[2][3]
        xVal = -pose[0][3]

        if (abs(lastPose - xVal) < 0.1 and abs(lastPose - yVal) < 0.1):
            break
        
        rPower, lPower = getPower(xVal)
        rRatio = rPower * 25
        lPower = lPower * 25
        
        lMotor.forward(lPower)
        rMotor.forward(rPower)
    lMotor.forward(0)
    rMotor.forward(0)


if (__name__== "__main__"):
    main()