import socket
import time
import csv
import cv2
import os
import time
from datetime import datetime
import errno 
import pyrebase
import requests
import json

HOST = '0.0.0.0'
PORT = 3220
path = "/home/afoflinux/Desktop/vertical_farming/check"
os.chdir(path)

# // Import the functions you need from the SDKs you need
# import { initializeApp } from "firebase/app";
# import { getAnalytics } from "firebase/analytics";
# // TODO: Add SDKs for Firebase products that you want to use
# // https://firebase.google.com/docs/web/setup#available-libraries
# // Your web app's Firebase configuration
# // For Firebase JS SDK v7.20.0 and later, measurementId is optional
# const firebaseConfig = {
#   apiKey: "AIzaSyAHMOfdcA8pOGivRPwFeRn_RdyB8SGXcEI",
#   authDomain: "verticalfarming-6c430.firebaseapp.com",
#   databaseURL: "https://verticalfarming-6c430-default-rtdb.firebaseio.com",
#   projectId: "verticalfarming-6c430",
#   storageBucket: "verticalfarming-6c430.appspot.com",
#   messagingSenderId: "826861288372",
#   appId: "1:826861288372:web:a5fc1c37dc483941e750e1",
#   measurementId: "G-PQM2VPD4ZB"
# };
# Initialize Firebase
# const app = initializeApp(firebaseConfig);
# const analytics = getAnalytics(app);


def request_image(data):
    url_photo = 'http://0.0.0.0:8000/plant/'

    files = {'file': open(data, 'rb')}
    response = requests.post(url_photo, files=files)
    try:
        json_data = json.loads(response.text)
        return json_data['plant']
    except:
        return None

def appendcsv (filename, csvrow):
    with open(filename, 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(csvrow)


# ###### FIREBASE ###########
# def sendcloud(filename):
#     config = {
#         "apiKey": "AIzaSyAHMOfdcA8pOGivRPwFeRn_RdyB8SGXcEI",
#         "authDomain": "verticalfarming-6c430.firebaseapp.com",
#         "databaseURL": "https://verticalfarming-6c430-default-rtdb.firebaseio.com",
#         "projectId": "verticalfarming-6c430",
#         "storageBucket": "verticalfarming-6c430.appspot.com",
#         "messagingSenderId": "826861288372",
#         "appId": "1:826861288372:web:a5fc1c37dc483941e750e1",
#         "measurementId": "G-PQM2VPD4ZB" 
#     }

#     firebase = pyrebase.initialize_app(config)
#     storage = firebase.storage()

#     path_on_cloud = "images/basil/image.jpeg"
#     path_local = filename
#     storage.child(path_on_cloud).put(path_local)
#     message = 'SomeInfoFromImage'
#     return message

if __name__ == '__main__':
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print("Server enabled")
            conn, addr = s.accept()
            # print(conn)
            with conn:
                print('Connected by: ', addr)
                while True:
                    # print('Firstly, here I am')
                    IBdata = conn.recv(1024)
                    # print(IBdata)
                    current_time = datetime.now()
                    current_time_str = current_time.strftime("%Y%m%d%H%M%S")
                    filename = 'Frame_'+current_time_str+'.jpeg'

                    # if IBdata:
                    rawdata = str(IBdata.decode('utf-8'))
                    i = 0

                    if rawdata == 'IsPressed':
                        video = cv2.VideoCapture(0)

                        while True:
                            ret, img = video.read()
                            #cv2.imshow('live video', img)
                            #filename = 'Frame_'+current_time_str+'.jpeg'
                            cv2.imwrite(filename, img)
                            res = request_image(filename)

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

                        # string lenght: 62 characters, sometimes it comes more than 1 at the time
                        ssize=int(len(rawdata)/62)
                        for x in range(ssize):
                            register = str(datetime.datetime.now())+","+rawdata[x*62:((x+1)*62)-1]
                            listdata = register.split(",")
                            print(listdata)
                            appendcsv("Enas_data.csv", listdata)
                        #conn.sendall("Ok".encode('utf8'))
                        time.sleep(0.1)
                
                    try:
                        #message = sendcloud(filename)
                        message = 'Image2Cloud'
                        print('Image sent to Cloud')
                        MESSAGE = message.encode('utf8')
                        conn.sendall(MESSAGE)
                        print('Info from image sent to Client')
                    except:
                        print("Cannot send the message")

                conn.close()
                print("Connection closed!")

    except:
        print("Cannot connect to the server")