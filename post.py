
import requests
import cv2
import json

def request_image(data):
    url_photo = 'http://0.0.0.0:8000/check_liveness/'

    files = {'file': open(data, 'rb')}
    response = requests.post(url_photo, files=files)
    try:
        json_data = json.loads(response.text)
        return json_data['liveness']
    except:
        return None

if __name__ == "__main__":
    path = '/home/bzwayne/Desktop/Liveness/liveness_tengri/ang.jpeg'
    res = request_image(path)
    print(res)