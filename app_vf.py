import os
import cv2
import time
from datetime import datetime
import socket
from fastapi import FastAPI,

path = "/home/afoflinux/Desktop/vertical_farming/check"
os.chdir(path)
i = 0

def appendcsv (filename, csvrow):
    with open(filename, 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(csvrow)


HOST = '0.0.0.0'
PORT = 3220

if __name__ == '__main__':
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print("Server enabled")
            conn, addr = s.accept()
            with conn:
                print('Connected by: ', addr)
                while True:
                    ##print('Firstly, here I am')
                    IBdata = conn.recv(1024)
                    current_time = datetime.now()
                    current_time_str = current_time.strftime("%Y_%m_%d_%H_%M_%S")
                    ##print('here I am 2')

                    if IBdata:
                        rawdata = str(IBdata.decode('utf8'))
                        # print(rawdata)

                        if rawdata == 'IsPressed':
                            video = cv2.VideoCapture(0)

                            while True:
                                ret, img = video.read()
                                cv2.imshow('live video', img)
                                filename = 'Frame_'+current_time_str+'.jpeg'
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
                        msg = "hiiiiii"
                        MESSAGE = msg.encode('utf-8')
                        conn.sendall(MESSAGE)
                    except:
                        print("Cannot send the message")

                conn.close()
                print("Connection closed!")

    except:
        print("Cannot connect to the server")
