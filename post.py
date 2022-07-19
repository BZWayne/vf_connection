import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json

def request(data):
    url = 'http://0.0.0.0:8000/plant'

    files = {'file': open(data, 'rb')}
    response = requests.post(url, files=files, verify = False)
    try:
        json_data = json.loads(response.text)
        return json_data
    except:
        return None

if __name__ == "__main__":
    path = '/home/afoflinux/Desktop/vertical_farming/check/Frame.jpeg'
    res = request(path)
    print(res)