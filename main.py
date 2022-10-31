import sys
from pickle import loads
import codecs

sys.path.append("../AprilTag/scripts")

import apriltag_video

funcPaths = ["./t_x.pickle", "./t_y.pickle", "./x_t.pickle", "./y_t.pickle"]

def main():
    funcsParsed = {}
    for func in funcPaths:
        with open(func, 'rb') as f:
            obj = loads(codecs.decode(f.read(), "base64"))
            funcsParsed[func] = obj
    for res in apriltag_video.apriltag_video(input_streams=[0]):
        print(res)

if __name__ == '__main__':
    main()