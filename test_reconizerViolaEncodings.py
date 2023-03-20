""" Facial Recognizer
This script performs face recognition using the 
face database generated by trainer.py.
For face detection, this script use haarcascades proposed by
Paul Viola and Michael Jones in their paper, 
"Rapid Object Detection using a Boosted Cascade of Simple Features" 
in 2001.
The algorithm used is based on ResNet-34 from 
the Deep Residual Learning for Image Recognition paper 
(https://arxiv.org/pdf/1512.03385.pdf) by He et al., 2015.
The network was trained by Davis King, the creator of 
dlib library.
(http://blog.dlib.net/2017/02/high-quality-face-recognition-with-deep.html)
Acording to Davis, the network was trained from scratch 
on a dataset of about 3 million faces and the pretrained 
model is in the public domain. Also, the model has an 
accuracy of 99.38% on the standard Labeled Faces in the 
Wild benchmark, i.e. given two face images, it correctly 
predicts if the images are of the same person 99.38% of 
the time.
Also, this script make use of face_recogniton module,
created by Adam Geitgey.
(https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78)
In his article, he describe the whole process for face 
recognition.
All this information, and more, can be found in this greate
article: https://pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
by Adrian Rosebrock.
"""

import imutils
import cv2
import face_recognition
import pickle
import os
from server_connection import send_encodings

#from smbus import SMBus
from itertools import cycle
from time import sleep

#SERVER
URL_SERVER = 'http://140.84.179.17:80'
PAGE = "/encodings"


# set 1 for macOS, maybe 2 for windows and others
#capture = cv2.VideoCapture(1)
capture = cv2.VideoCapture(0)

# load haar cascade de
haarCascade = 'D:\\RICARDO\\Escritorio\\upiita\\SEMESTRE 10\\TT2\\RasberryPi codes\\TT_RaspberryPi\\haarcascade_frontalface_default.xml'  
#haarCascade = '/home/ricardo/TT_tests/haarcascade_frontalface_default.xml'  #for rasppi

face_cascade = cv2.CascadeClassifier(haarCascade)

while (capture.isOpened()):
    ret, image = capture.read()

    image = imutils.resize(image, width=600)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # for haar cascade

    # detect face using haar cascades
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    rects = []
    # convert bounding boxes (x, y, w, h) to face locations in css (top, right, bottom, left) order
    for (x,y,w,h) in faces:
        rects.append([y, x+w, y+h, x])
    
    # get encoding of detected faces
    encodings = face_recognition.face_encodings(rgb, rects)

    #sending encodings
    send_encodings(URL_SERVER,PAGE,encodings)

    #print(encodings)

    userIDs = []
    
    id = "Unknownnn"

    # loop over the recognized faces
    for ((x1, y1, x2, y2), id) in zip(rects,id):
        # draw the predicted face id on the image
        cv2.rectangle(image, (y2, x1), (y1, x2), (0, 255, 0), 2)
        y = x1 - 15 if x1 - 15 > 15 else x1 + 15
        cv2.putText(image, id, (y2, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (0, 255, 0), 2)

    cv2.imshow('Recognizer', image)
    if (cv2.waitKey(1) == 27):
        break

capture.release()
