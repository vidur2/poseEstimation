from scipy.interpolate import splev
from math import e
from motor import Motor
import sys

sys.path.append("../AprilTag/scripts")

import apriltag_video

with open("./x_y.pickle", 'rb') as f:
    path = loads(codecs.decode(f.read(), "base64"))

path = None
maxPowah = 1

def curvature(currX, currY):
    yDoublePrime = splev(currX, path["diff2"])
    yPrime = splev(currX, path["diff"])

    return yDoublePrime/((1+(yPrime)**2)**(3/2))

def transform(kappa):
    return e**(-kappa) * maxPowah

def adjPower(curvature):
    if (curvature >= 0):
        return (maxPowah, transform(curvature))
    else:
        return (transform(curvature), maxPowah)

def getPower(currX, currY):
    kappa = curvature(currX, currY)
    return adjPower(kappa)

def main():
    lastPose = path["lastPose"]
    lMotor = Motor(16, 25, 12, False)
    rMotor = Motor(5, 6, 13, True)
    for pos in apriltag_video.apriltag_video([0]):
        yVal = pose[2][3]
        xVal = pose[0][3]

        if (abs(lastPose - xVal) < 0.1 and abs(lastPose - yVal) < 0.1):
            break
        
        rPower, lPower = getPower(xVal, yVal)

        lMotor.forward(lPower)
        rMotor.forward(rPower)


if (__name__== "__main__"):
    main()