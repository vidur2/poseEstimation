from scipy.interpolate import splev
from math import e
from motor import Motor

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
    with open("./x_y.pickle", 'rb') as f:
        path = loads(codecs.decode(f.read(), "base64"))


if (__name__== "__main__"):
    main()