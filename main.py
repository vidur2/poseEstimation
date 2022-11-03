import sys
from pickle import loads
import codecs
from scipy.interpolate import splev

sys.path.append("../AprilTag/scripts")

import apriltag_video

funcPaths = ["./t_x.pickle", "./t_y.pickle", "./x_t.pickle", "./y_t.pickle"]
err = 0.5

def main():
    funcsParsed = {}
    for func in funcPaths:
        with open(func, 'rb') as f:
            obj = loads(codecs.decode(f.read(), "base64"))
            funcsParsed[func] = obj
    print(splev(0, funcsParsed["./t_x.pickle"]["self"]))
    # for res in apriltag_video.apriltag_video(input_streams=[0]):
    #     pose = res[1]
    #     tEq = splev(pose[0], obj["t_x"]["self"])
    #     tVer = splev(pose[1], obj["t_y"]["self"])
    #     xSpeed= splev(tEq, obj["x_t"]["diff"])
    #     ySpeed = splev(tVer, obj["y_t"]["diff"])

if __name__ == '__main__':
    main()