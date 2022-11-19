import numpy as np
from numpy.polynomial import Chebyshev
from flask import Flask, request
import json
import sys
from enum import Enum
import pickle
import codecs
from math import cos, sin
from xyCoord import XyCoord
# import matplotlib.pyplot as plt

app = Flask(__name__)

from scipy.interpolate import splprep, splev, splder, splrep, BSpline

def writeToFile(obj, fileName):
    print(obj)
    with open(f"./{fileName}.pickle", 'wb') as f:
        f.write(codecs.encode(pickle.dumps(obj), "base64"))

def sortList(xArr, yArr):
    stack = [XyCoord(x, y) for x, y in zip(xArr, yArr)]
    stack.sort()

    return [i.x for i in stack], [i.y for i in stack]

@app.route("/", methods=["POST"])
def index():
    body = json.loads(json.loads(request.get_data()))
    graph_type = body["type"]
    x_arr = body["a"]
    y_arr = body["b"]


    der = None
    tck = None
    diff = False
    der2 = None
    lastPose = None
    if (graph_type[len(graph_type) - 1] == 't' or graph_type == 'x_y'):
        diff = True
        if graph_type == 'x_y':
            x_arr, y_arr = sortList(x_arr, y_arr)
        tck = splrep(x_arr, y_arr, s = 0)
        splder(tck)
        der = BSpline(t=tck[0], c=tck[1], k=tck[2]).derivative(1)
        der2 = BSpline(t=tck[0], c=tck[1], k=tck[2]).derivative(2)
        lastPose = (x_arr[len(x_arr) - 1], y_arr[len(y_arr) - 1])
    else:
        tck, u = splprep([x_arr, y_arr], s=0)
    

    # writeToFile({
    #         "self": tck,
    #         "diff": der,
    #         "diff2": der2
    #     }, 
    #     graph_type
    # )
    with open(f"./{graph_type}.pickle", 'wb') as f:
        spline_out = {
            "self": tck,
            "diff": der,
            "diff2": der2,
            "lastPose": lastPose
        }
        f.write(codecs.encode(pickle.dumps(spline_out), "base64"))
    return "good"

@app.route("/aprilPos", methods=["POST"])
def loadTransMatrix():
    body = json.loads(request.get_data())

    aprilPose = body["aprilPose"]

    tagOut = {}
    for tag in aprilPose:

        # Defining translation matrix
        translMatrix = np.eye(2)
        translMatrix[0][1] = tag["y"]
        translMatrix[1][0] = tag["x"]

        # Defining Rotation matrix
        deg = None

        if (tag["rotation"] == "R"):
            deg = 0
            pass
        elif (tag["rotation"] == "L"):
            deg = 180
            pass
        elif (tag["rotation"] == "U"):
            deg = 90
            pass
        else:
            deg = 270
            pass
        rotMatrix = np.array([
            [cos(deg), -sin(deg)],
            [sin(deg), cos(deg)]
        ])

        tagOut[tag["id"]] = rotMatrix * translMatrix
    writeToFile(tagOut, "aprilPose")
    return "good"

if (__name__ == "__main__"):
    app.run(port = 5001)