import cv2
import socket
import time
import threading
import imutils
import time
import uvicorn
from multiprocessing import Process, Queue
import subprocess
import numpy as np
from datetime import datetime
from imutils.video import VideoStreams
from fastapi import FastAPI, Request, status
from fastapi.responses import StreamingResponse
from fastapi.encoders import jsonable_encoder

path = "/home/afoflinux/Desktop/vertical_farming/check"
i = 0
HOST = '0.0.0.0'
PORT = 3220
url_rtsp = 0
lock = threading.Lock()
app = FastAPI()

manager = None
count_keep_alive = 0

width = 1280
height = 720

def picture():
    current_time = datetime.now()
    current_time_str = current_time.strftime("%Y_%m_%d_%H_%M_%S")
    video = cv2.VideoCapture(0)
    i = 0
    while True:
        ret, img = video.read()
        cv2.imshow('live video', img)
        filename = path + '/' + 'Frame_'+current_time_str+'.jpeg'
        # filename = path + '/' + 'frame.jpeg'
        cv2.imwrite(filename, img)
        i = i+1
        key = cv2.waitKey(100)
        if key == ord('q'):
            break
        if i == 1:
            i = 0
            break
    # close the camera
    video.release()
    cv2.destroyAllWindows()

def start_stream(url_rtsp, manager):
    global width
    global height

    vs = VideoStream(url_rtsp).start()
    while True:
        time.sleep(0.2)

        frame = vs.read()
        frame = imutils.resize(frame, width=680)
        output_frame = frame.copy()

        if output_frame is None:
            continue
        (flag, encodedImage) = cv2.imencode(".jpg", output_frame)
        if not flag:
            continue
        manager.put(encodedImage)


def streamer():
    try:
        while manager:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(manager.get()) + b'\r\n')
    except GeneratorExit:
        print("cancelled")


def manager_keep_alive(p):
    global count_keep_alive
    global manager
    while count_keep_alive:
        time.sleep(1)
        print(count_keep_alive)
        count_keep_alive -= 1
    p.kill()
    time.sleep(.5)
    p.close()
    manager.close()
    manager = None

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/", status_code = status.HTTP_201_CREATED)
async def plant():
    try:
        picture()
        return {'plant':'received'}
    except:
        return {'plant':'NOT received'}

async def video_feed():
    return StreamingResponse(streamer(), media_type="multipart/x-mixed-replace;boundary=frame")

@app.get("/keep-alive")
def keep_alive():
    global manager
    global count_keep_alive
    count_keep_alive = 100
    if not manager:
        manager = Queue()
        p = Process(target=start_stream, args=(url_rtsp, manager,))
        p.start()
        threading.Thread(target=manager_keep_alive, args=(p,)).start()

# if __name__ == '__main__':
#     uvicorn.run(app, host=HOST, port=PORT)