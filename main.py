import sys
from pickle import loads
import codecs
from scipy.interpolate import splev
import numpy as np

sys.path.append("../AprilTag/scripts")

import apriltag_video
from networktables import NetworkTables, NetworkTablesInstance

funcPaths = ["./t_x.pickle", "./t_y.pickle", "./x_t.pickle", "./y_t.pickle"]
matrixPath = ["./aprilPose.pickle"]
err = 0.5

NetworkTables.initialize(server="10.51.09.2")

def initializeNtwrk():
    ntwrkInst = NetworkTablesInstance.create()
    table = ntwrkInst.getTable(key="SmartDashboard")
    return table

def main():
    
    sd = initializeNtwrk()


    funcsParsed = {}
    for func in funcPaths:
        with open(func, 'rb') as f:
            obj = loads(codecs.decode(f.read(), "base64"))
            funcsParsed[func] = obj

    # offset = None
    # with open(matrixPath, 'rb') as f:
    #     offset = loads(codecs.decode(f.read(), "base64"))

    # alignToStart()
    for res in apriltag_video.apriltag_video(input_streams=[0]):
        if (len(res)):
            pose = res[1]
            yVal = pose[2][3]
            xVal = pose[0][3]

            # TODO multpily by transformation here
            # print((wxVal, yVal))  
            tEq = splev(xVal, funcsParsed["./t_x.pickle"]["self"])
            tVer = splev(yVal, funcsParsed["./t_y.pickle"]["self"])
            xSpeed= splev(tEq, funcsParsed["./x_t.pickle"]["diff"])
            ySpeed = splev(tVer, funcsParsed["./y_t.pickle"]["diff"])

            sd.putNumber("xSpeed", xSpeed)
            sd.putNumber("ySpeed", ySpeed)

def alignToStart(obj):
    targetX = splev(0, obj["x_t"]["self"])
    targetY = splev(0, obj["y_t"]["self"])
    for pose in apriltag_video.apriltag(input_streams=[0]):
        velX = -(pose[0] - targetX)
        velY = -(pose[1] - targetY)

        # TODO send values over NT

        if (abs(velX) < .1 and abs(velY) < .1):
            return

if __name__ == '__main__':
    main()