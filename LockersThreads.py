""" Facial Detection for Lockers RaspberryPi
This script performs the face detection, this script use haarcascades proposed by
Paul Viola and Michael Jones in their paper, 
"Rapid Object Detection using a Boosted Cascade of Simple Features" 
in 2001.
When a face is detected the is used the face_recognition module created by Adam Geitgey to 
obtain the encoding for the face and then the information is sended using the function send_encodings
from the server_connection.py, the value returned is the name of the person (if exists in the database).
"""

'''
In this script Threads are used to run the face detection and use the getEncodings function

'''

import imutils
import cv2
import face_recognition
import pickle
import os
from server_connection import send_encodingsLockers, updateDB, checkLocker
import json
from flask import request
from lockers_functions import openLocker
import threading
#from server_connection import getAllLockers
from ast import literal_eval

# Libraries for I2C Configuration
from smbus import SMBus
from itertools import cycle
from time import sleep

# Bus Configuration for I2C Communication
bus = SMBus(1) # Port 1 used on REV2 
bus.write_byte(0x38,0x00)   # All the ports in LOW

# Variable declaration
userIDs = []
detectFace = True
idname = []


# SERVER DIRECTION
URL_SERVER = 'http://140.84.179.17:80'
PAGE = "/encodings"

def rec_function(encodings):
    global idname
    userIDs = []
    print("Reconociendo...")

    # Sending encodings and getting ID
    r=send_encodingsLockers(URL_SERVER,PAGE,encodings)

    res= r['message'] # Checking the response in the JSON 


    # Is the user found? 
    if res=='UserNoFound':
        idname=['Usuario no encontrado'] # ID NAME 
        

    elif res=='FACE RECOGNITION ERROR': # Face recognition error
        idname=['FACE RECOGNITION ERROR']         

    else:
        id_name=(r["person"]["FirstName"]) # Extracting the ID from the json response
        id_lastname=(r["person"]["LastName"])
        idname=[(id_name+' '+id_lastname)] # ID NAME
        id=(r['person']['UserID']) # UserID NUMBER
        
        
        # OPEN LOCKER FUNCTIONS 

        lockerfree=checkLocker(id)  # Getting LOCKER ID
        lockerO=lockerfree['LockerFree']['LockerID']    # Selecting LockerID
        hex_lock=literal_eval(lockerO)  # Converting str to hex integer

        openflag=lockerfree['Openflag'] # Getiing value Openflag 

        # When Openflag = 0: The USER Does not have any locker so automatically assign a Locker --> Option to Open locker
        # When Openflag = 1: Ther USER already have a locker so is able to :
        #       --> Option to Open locker and still using it 
        #       --> Option to Open locker and leave the laboratory 
        # Openflag is sent by a query from the API to the DB
        if openflag==0:
            #OPEN LOCKER?
            print("Do you want to open your locker?\n")
            resLock=input("Y or N")

            if resLock=='Y':
                openLocker(hex_lock)    # Calling function to open the locker
                # updateDB (UserID, LockerID, leaveflag)  
                # leaveflag = 1 when the User will use again the locker
                updateDB(id, lockerO, 1)   # Updating the TALKE LockersUsers with UserID, LockerID, DATE, TIME
                print("User registered successfully")
            else:
                print("Thank you")
                    
        else: 
            print("Do you want to open your locker (Press=O or Open and Leave (L)?\n")
            resLock=input("O or L")
            if resLock=='O':
                openLocker(hex_lock)    # Calling function to open the locker
                # leaveflag = 1 when the User will use again the locker
                updateDB(id, lockerO, 1)   # Updating the TABLE LockersUsers with UserID, LockerID, DATE, TIME
                print("User registered successfully")
            elif resLock=='L':
                openLocker(hex_lock)    # Calling function to open the locker
                # leaveflag = 2 when the User wont use again the locker (Leave the laboratory)
                updateDB(id, lockerO, 2)   # Updating the TABLE LockersUsers with UserID, LockerID, DATE, TIME

            else:
                print("incorrect answer")
                    
    print("Reconocido!")


capture = cv2.VideoCapture(0)   # 0 for raspi

# load the faces database
print("Loading faces database...")

# load haar cascade
haarCascade = '/home/ricardo/TT_tests/haarcascade_frontalface_default.xml'  #for raspi
'''haarCascade = os.path.join(file_dir, haarCascade)
haarCascade = os.path.abspath(os.path.realpath(haarCascade))'''
face_cascade = cv2.CascadeClassifier(haarCascade)

while (capture.isOpened()):
    ret, image = capture.read()

    image = imutils.resize(image, width=600)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # for haar cascade

    # Detect face using haar cascades
    faces = face_cascade.detectMultiScale(
        gray, 
        scaleFactor=1.3, 
        minNeighbors=5,
        minSize=(190,190))  # Modify the distance to detect a face

    rects = []

    # convert bounding boxes (x, y, w, h) to face locations in css (top, right, bottom, left) order
    for (x,y,w,h) in faces:
        rects.append([y, x+w, y+h, x])
        
    #print(detectFace)
    
    if len(faces) == 0:
        rects = []
        idname = []
        detectFace = True
    
    if detectFace == True and len(faces) != 0:
        # get encoding of detected faces
        encodings = face_recognition.face_encodings(rgb, rects)
        
        x = threading.Thread(target=rec_function, args=(encodings,), daemon=True)
        x.start()
        detectFace = False
        
        
    if len(idname) > 0:
        # The loop over the recognized faces is cancelled but the video has a delay when a face is detected
        # When the loop is activated the delay dissapear --> NEED TO BE CHECKED
        #for ((x1, y1, x2, y2), idname) in zip(rects, idname):
        finalid=idname[0]
            # draw the predicted face id on the image
        cv2.rectangle(image, (y2, x1), (y1, x2), (0, 255, 0), 2)
        y = x1 - 15 if x1 - 15 > 15 else x1 + 15
        cv2.putText(image, finalid, (y2, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (0, 255, 0), 2)
    else:
        
        for (x1, y1, x2, y2) in rects:
            # draw the predicted face id on the image
            cv2.rectangle(image,(y2, x1), (y1, x2), ( 0,0, 255), 2)
            
    cv2.imshow('Recognizer', image)
    if (cv2.waitKey(1) == 27):
        break

capture.release()
cv2.destroyAllWindows()