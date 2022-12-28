import cv2
from cv2 import *
import time
import time
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, true
import requests

import base64  # is to convert image into base64 hexadecimal
static_back = None
motion_list = [None, None]
time = []
video = cv2.VideoCapture(0)

# Infinite while loop to treat stack of image as video
while True:
    check, frame = video.read()
    motion = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if static_back is None:
        static_back = gray
        continue

    diff_frame = cv2.absdiff(static_back, gray)

    thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    cnts, _ = cv2.findContours(thresh_frame.copy(),
                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        motion = 1

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    motion_list.append(motion)
    motion_list = motion_list[-2:]

    # Appending Start time of motion
    if motion_list[-1] == 1 and motion_list[-2] == 0:

        url = 'http://localhost:3001/motion_detector'

        date_time = datetime.now().strftime("%m-%d-%Y, %H-%M-%S")
        print(date_time)

        final_name = date_time + '.png'
        result, image = video.read() 
        cv2.imwrite(final_name, image) 

        with open(final_name, "rb") as f:  
            png_encoded = base64.b64encode(
                f.read()) 
            print(png_encoded)

        myobj = {'Time_Captured': str(
            datetime.now()), 'image': png_encoded}
        requests.post(url, data=myobj)

    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Difference Frame", diff_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)
    if key == ord('n'):
        break

video.release()
