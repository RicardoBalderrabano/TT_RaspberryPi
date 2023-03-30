""" Facial Detection
This script performs the face detection, this script use haarcascades proposed by
Paul Viola and Michael Jones in their paper, 
"Rapid Object Detection using a Boosted Cascade of Simple Features" 
in 2001.
When a face is detected the is used the face_recognition module created by Adam Geitgey to 
obtain the encoding for the face and then the information is sended using the function send_encodings
from the server_connection.py, the value returned is the name of the person (if exists in the database).
"""

import imutils
import cv2
import face_recognition
import pickle
import os
from server_connection import send_encodings
import json
from flask import request

#from smbus import SMBus
from itertools import cycle
from time import sleep

#SERVER DIRECTION
URL_SERVER = 'http://140.84.179.17:80'
PAGE = "/encodings"

capture = cv2.VideoCapture(0) #0 for raspi

# Load haar cascade file
#haarCascade = 'D:\\RICARDO\\Escritorio\\upiita\\SEMESTRE 10\\TT2\\RasberryPi codes\\TT_RaspberryPi\\haarcascade_frontalface_default.xml'  
haarCascade = '/home/ricardo/TT_tests/haarcascade_frontalface_default.xml'  #for raspi

face_cascade = cv2.CascadeClassifier(haarCascade)

# Face detected flag
face_detected=False

while True:

    capture.isOpened()  # OPEN CAMERA

    ret, image = capture.read()

    image = imutils.resize(image, width=600)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # For haar cascade

    # Detect face using haar cascades
    faces = face_cascade.detectMultiScale(
        gray, 
        scaleFactor=1.3, 
        minNeighbors=5,
        minSize=(190,190))
    
    if len(faces)>0:
        face_detected=True
        rects = []
        # Convert bounding boxes (x, y, w, h) to face locations in css (top, right, bottom, left) order
        for (x,y,w,h) in faces:
            rects.append([y, x+w, y+h, x])
        
        # Get encoding of detected faces
        encodings = face_recognition.face_encodings(rgb, rects)

        # Sending encodings and getting ID
        r=send_encodings(URL_SERVER,PAGE,encodings)
        
        res= r['message'] #Checking the response in the JSON 

        #Is the user found? 
        if res=='UserNoFound':
            id=['Usuario no encontrado']
        else:
            id_name=(r['person']['FirstName']) #Extracting the ID from the json response
            id_lastname=(r["person"]["LastName"])
            id=[(id_name+' '+id_lastname)]
        
        userIDs = []
        
        # Loop over the recognized faces
        for ((x1, y1, x2, y2), id) in zip(rects,id):
            # draw the predicted face id on the image
            cv2.rectangle(image, (y2, x1), (y1, x2), (0, 255, 0), 2)
            y = x1 - 15 if x1 - 15 > 15 else x1 + 15
            cv2.putText(image, id, (y2, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)
        cv2.imshow('Recognizer', image)
        if (cv2.waitKey(1) == 27):
            break
    else:
        face_detected=False
        cv2.imshow('Recognizer', image)
        if (cv2.waitKey(1) == 27):
            break

capture.release()
