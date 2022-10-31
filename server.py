import numpy as np
from numpy.polynomial import Chebyshev
from flask import Flask, request
import json
import sys
from enum import Enum
import pickle
import codecs
# import matplotlib.pyplot as plt

app = Flask(__name__)

from scipy.interpolate import splprep, splev, splder, splrep, BSpline

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

    with open(f"./{graph_type}.pickle", 'wb') as f:
        spline_out = {
            "self": tck,
            "diff": der
        }
        # print(spline_out)
        f.write(codecs.encode(pickle.dumps(spline_out), "base64"))


    return "good"


if (__name__ == "__main__"):
    app.run(port = 5001)