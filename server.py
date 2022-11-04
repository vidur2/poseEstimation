import numpy as np
from numpy.polynomial import Chebyshev
from flask import Flask, request
import json
import sys
from enum import Enum
import pickle
import codecs
from math import cos, sin
# import matplotlib.pyplot as plt

app = Flask(__name__)

from scipy.interpolate import splprep, splev, splder, splrep, BSpline

def writeToFile(obj, fileName):
    with open(f"./{fileName}.pickle", 'wb') as f:
        f.write(codecs.encode(pickle.dumps(obj), "base64"))

@app.route("/", methods=["POST"])
def index():
    body = json.loads(json.loads(request.get_data()))
    graph_type = body["type"]
    x_arr = body["a"]
    y_arr = body["b"]


    der = None
    tck = None
    diff = False
    if (graph_type[len(graph_type) - 1] == 't'):
        diff = True
        tck = splrep(x_arr, y_arr, s = 0)
        splder(tck)
        der = BSpline(t=tck[0], c=tck[1], k=tck[2]).derivative(1)
    else:
        tck, u = splprep([x_arr, y_arr], s=0)
    

    writeToFile({
            "self": tck,
            "diff": der
        }, 
        graph_type
    )
    with open(f"./{graph_type}.pickle", 'wb') as f:
        spline_out = {
            "self": tck,
            "diff": der
        }
        f.write(codecs.encode(pickle.dumps(spline_out), "base64"))
    return "good"

@app.route("/aprilPos", methods=["POST"])
def loadTransMatrix():
    body = json.loads(json.loads(request.get_data()))

    aprilPose = body["aprilPose"]

    tagOut = {}
    for tag in aprilPose:

        # Defining translation matrix
        translMatrix = np.eye(2)
        translMatrix[0][1] = tag["y_val"]
        translMatrix[1][0] = tag["x_val"]

        # Defining Rotation matrix
        deg = None

        if (tag["orientation"] == "R"):
            deg = 0
            pass
        elif (tag["orientation"] == "L"):
            deg = 180
            pass
        elif (tag["orientation"] == "U"):
            deg = 90
            pass
        else:
            deg = 270
            pass
        rotMatrix = np.arr([
            [cos(deg), -sin(deg)],
            [sin(deg), cos(deg)]
        ])

        tagOut[tag["id"]] = rotMatrix * translMatrix
    writeToFile(tagOut, "aprilPose")
    return "good"

if (__name__ == "__main__"):
    app.run(port = 5001)