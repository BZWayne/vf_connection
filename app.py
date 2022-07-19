import cv2
import socket
import time
from datetime import datetime
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
import numpy as np

path = "/home/afoflinux/Desktop/vertical_farming/check"
i = 0
HOST = '0.0.0.0'
PORT = 3220
alpha = 2.0 # Simple contrast control
beta = 15    # Simple brightness control

def picture():
    current_time = datetime.now()
    current_time_str = current_time.strftime("%Y_%m_%d_%H_%M_%S")
    video = cv2.VideoCapture(0)
    i = 0
    while True:
        ret, img = video.read()
        new_image = np.zeros(img.shape, img.dtype)
        # dst = cv2.detailEnhance(img, sigma_s=10, sigma_r=0.15)
        #cv2.imshow('live video', img)
        filename = path + '/' + 'Frame.jpeg'
        # filename = path + '/' + 'frame.jpeg'

        # print(' Basic Linear Transforms ')
        # print('-------------------------')
        # try:
        #     alpha = float(input('* Enter the alpha value [1.0-3.0]: '))
        #     beta = int(input('* Enter the beta value [0-100]: '))
        # except ValueError:
        #     print('Error, not a number')

        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                for c in range(img.shape[2]):
                    new_image[y,x,c] = np.clip(alpha*img[y,x,c] + beta, 0, 255)

        cv2.imwrite(filename, new_image)
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

app = FastAPI()

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


# if __name__ == '__main__':
#     uvicorn.run(app, host=HOST, port=PORT)