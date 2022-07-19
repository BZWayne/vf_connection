import os
import cv2
import numpy as np
import argparse
import warnings
import time
import math
from flask import Flask, render_template, Response, stream_with_context
from flask_socketio import SocketIO, emit
import datetime
import json
import requests
from flask import request
from flask import jsonify
import atexit
warnings.filterwarnings('ignore')

################## SERVER ADDRESS ###################
HOST = '0.0.0.0'
PORT = 3220
app = Flask(__name__)
camera = cv2.VideoCapture(0)

################## PICTURE PATH ######################
path = "/home/afoflinux/Desktop/vertical_farming/check"
os.chdir(path)
i = 0
######################################################


def appendcsv (filename, csvrow):
    with open(filename, 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(csvrow)


def gen_frames():  # generate frame by frame from camera
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 


@app.route('/')
def index():
    return render_template('index_test.html')
    

@app.route('/video_feed')
# @app.route('/video_feed', methods=['GET', 'POST'])
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host=HOST, debug=True, use_reloader=False)
    # app.run(debug=True)