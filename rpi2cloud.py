import socket
import time
import csv
import cv2
import os
import time
from datetime import datetime
from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
import os

HOST = '0.0.0.0'
PORT = 3220
path = "/home/afoflinux/Desktop/vertical_farming/check"
os.chdir(path)

def google_cloud(filename):
    credentials_dict = {
        "type": "service_account",
        "project_id": "verticalfarming-356807",
        "private_key_id": "d216c049547a20e2bb4e1cfb6edc7a9a623dd591",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDWXNUCjeY6yxZh\nPOkfcrX5tieYeA9/+zokej/5Q0Gg0skMGy/MhpDOk6PHhAJ0KVhr8NU7Lu8ftvud\nlvMe62W4wFTAClq5KdWf/UQnkQZ0pxeJ4ojVOuGOkndjkko9y3j2EuURZYKYsxAC\n6ipu5+iWEKCth3mktUqtIksCSICywvKmcFIDu7yZ1VT2lZO+QX1cFaO5V3Bov2ep\nOuk/CZDdm2aagpikzwgFB730dHAxxjxm/UR/Dy5j1xtiA0c/8FjFLkL43CoCq5c1\nuRM7xKmgGaVtP5kiH9gT5knhxtQ+mGrmdleuOsw810rZYXvUTienLPKpZdTCS1Fl\nmIeRw2YVAgMBAAECggEAB7dJt5DSA7XBtXhSz936LOXgoP1ZWXr6icuYt+ky2I4d\nzIDCBLOnTLhFwe2/hNzkIOaHVl0HIHYesnp3f9prS+4oXs1AnL+jv+GG7YGr4NEO\n6Nitojc/XTlqcLwYTgcf8IOXmTu1KrfvUJuLMXjJh3VLw1NIDqSz7m14k7l2YHjR\nAzd2sKPEVUpQCITbavEGegzhZaBHQfyyLnvPbRbUak0/wF64PVVGdwsYbhWhEKRt\nAJ3c7D0p3v7shCxduwDBFF7inO1bL/4gYQC5CdZ9bTSQAvgboEWTZZxZI+sZK+SQ\noo/krUe4H7CZyDvcwW8aA+RdnJ6dIVV4f8eNHH20VQKBgQD/wNUvsw7voz9EZwAt\nsMrbDEp0kH0+/REzFnS4IHlJWs/njhsLPSLCvhrLywiKZuOlvUWYpl9TCYVFTflQ\n06GdJLUnL+rhOzEz99v6OHBTEKorjyytzzJaOH4qRtQxDMLfJlpwbHLjHRyvsN22\nT2b3TJSrW13ssY8tO/MMhPxecwKBgQDWkcbE+ergmWfMwPjrOqsc0r0+u0gjES3q\nby4qE5NDX3Qhp1Ibj6lBApr2KFRw4uxk2PBCrc/bxQSDl5QepOcWOlvrFF4eM4fN\ny3jR+s64epnGiKe+rke1SnNvxeVjYrJvvQNaDYoeXPbkbXbAD5ucHZCgnmuON02T\nsdWRLvs/VwKBgHievK0DeS7iQkuDfJ0P/Yxz7oWtQ7S6bCs5ExFoF2vWTam65txV\nGBjayg6FkmCcCA+6BaHqDZk/K0C1drl9JoLTtjBmNBPH8/u7kV8g0TEL8gYbP4o1\n51yPukk8IIWFrD7Meuj87O5aY5YlB1wddMV7s75hmBmy4IEH/ihQbCorAoGAdLja\nWx7k0YdB+xVik3vXx5cwUWbJyCG5S5VtlIAPlQ/g+cmulcWhufaz24J25O3c0MNe\nd7dbol7bpMYZUk48U1At3oS26lD36FBuijOYrqwq6OA/+C+QXKOChmQt89Gl5bj5\nkMxavUevGvYdKj+TU+qVWXq0Yand7qFH33GiRYMCgYEA5tgnDH+PHV6Ldbavu8zu\n7O8L2i2OnAj5cizZoNwNAXwhHlC376Bl66SQye1ujc9h6zP3zuVimy/GtvxE6iU6\nSaqE5c/ILYKJownyOLKQ0X8xnkN5NojV5KjeptR47/BorcJMp4OclUgUU+f+bJcY\nIzhUCNsVfjBOZ4GZ4ynW9fw=\n-----END PRIVATE KEY-----\n",
        "client_email": "verticalfarming-356807@appspot.gserviceaccount.com",
        "client_id": "101084578763635294305",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/verticalfarming-356807%40appspot.gserviceaccount.com"
    }
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        credentials_dict
    )
    client = storage.Client(credentials=credentials, project='VerticalFarming')
    bucket = client.get_bucket('verticalfarming')
    blob = bucket.blob('myfile')
    blob.upload_from_filename(filename)
    message = 'Done'
    return message

def appendcsv (filename, csvrow):
    with open(filename, 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(csvrow)

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
                    rawdata = str(IBdata.decode('utf8'))
                    i = 0

                    if rawdata == 'IsPressed':
                        video = cv2.VideoCapture(0)

                        while True:
                            ret, img = video.read()
                            #cv2.imshow('live video', img)
                            #filename = 'Frame_'+current_time_str+'.jpeg'
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
                        #message = sendcloud(filename)
                        message = google_cloud(filename)
                        # message = 'Image2Cloud'
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