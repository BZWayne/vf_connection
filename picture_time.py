import cv2
import os
import time
from datetime import datetime

path = "/home/afoflinux/Desktop/vertical_farming/pictures"
 
os.chdir(path)
 
i = 20
wait = 0
 
video = cv2.VideoCapture(0)
 
while True:

    ret, img = video.read()
    #font = cv2.FONT_HERSHEY_PLAIN
    #cv2.putText(img, str(datetime.now()), (20, 40),
    #            font, 2, (255, 255, 255), 2, cv2.LINE_AA)
 
    # Display the image
    cv2.imshow('live video', img)
 
    key = cv2.waitKey(100)
 
    wait = wait+100
 
    if key == ord('q'):
        break
    # 3600000
    if wait == 3600000:
        filename = 'Frame_'+str(i)+'.jpeg'

        cv2.imwrite(filename, img)
        i = i+1
        wait = 0
 
# close the camera
video.release()
 
# close open windows
cv2.destroyAllWindows()