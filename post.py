import requests

# url = 'http://0.0.0.0:8000/'
# url = 'http://127.0.0.1:8000/'
# url = 'http://172.18.0.1:8000/file'
url = 'http://20.226.35.115:8000/'

##### send image client #######
def sendImage(filename):
    files = {'my_file': (filename, open(filename, 'rb'))}
    response = requests.post(url, files = files)
    message = response.json()
    print(message)
    # message = 'Successfully received answer from server'
    # return message

if __name__ == "__main__":
    filename = '/home/afoflinux/Desktop/vertical_farming/check/Frame.jpeg'
    sendImage(filename)