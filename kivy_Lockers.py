'''
This script performs the face detection, this script use haarcascades proposed by Paul Viola and Michael Jones in their paper, 
"Rapid Object Detection using a Boosted Cascade of Simple Features" in 2001.

KIVY - Is a framework for developing mobile apps and other multitouch application software with a natural user interface (NUI), 
    In this script is used to make a user interface deployed in a touch screen for the raspberry, this UI shows the video recording by
    the camera (Face detection and recognizion when a person stands in front) and 3 buttons used to Open/Leave/Cancel the automatic locker's lock. 

THREADS - A thread is implemented to run a face recognition function, this function make a query to the DB through an API using the encodings obtained
        when a face is detected. Recieves the UserID and Name (If it is founded) and make a new query to the LockersDB in order to check if the user
        has already a locker or not. 
            If the user has not a locker yet: "ABRIR LOCKER" or "CANCELAR" buttons can be used 
            If the user has already a locker: "ABIRI LOCKER", "LIBERAR LOCKER" or "CANCELAR" buttons can be used

Buttons - Each button has a function when are pressed, and it will Update a the DB to make a record when a locker is opened or freed

IMPORTANT: Before running in raspi run "export DISPLAY=:0"
'''
# DELAY WHEN BUTTON IS PRESSED
# DELAY WHEN FACE IS DETECTED
# ALL BUTTONS WORKING 

import os
os.environ['KIVY_GL_BACKEND'] = 'gl'
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import time
from kivy.uix.floatlayout import FloatLayout


# Face recognition and flask libraries
import cv2
import imutils
import face_recognition
from server_connection import send_encodingsLockers, updateDB, checkLocker
import json
from flask import request
from lockers_functions import openLocker
import threading
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


# SERVER DIRECTION
URL_SERVER = 'http://140.84.179.17:80'
PAGE = "/encodings"

# Load haar cascade file
#haarCascade = 'D:\\RICARDO\\Escritorio\\upiita\\SEMESTRE 10\\TT2\\RasberryPi codes\\TT_RaspberryPi\\haarcascade_frontalface_default.xml'  
haarCascade = '/home/ricardo/TT_tests/haarcascade_frontalface_default.xml'  #for raspi
face_cascade = cv2.CascadeClassifier(haarCascade)

# GLOBAL

buttonsFlag=0

def rec_function(encodings):
    global buttonsFlag
    global idname
    global hex_lock, lockerO, id, idname
    userIDs = []
    print("Reconociendo...")

    # Sending encodings and getting ID
    r=send_encodingsLockers(URL_SERVER,PAGE,encodings)

    res= r['message'] # Checking the response in the JSON 

    # Is the user found? 
    if res=='UserNoFound':                  # User no founded
        idname=['Usuario no encontrado']    # ID NAME 
        
    elif res=='FACE RECOGNITION ERROR':     # Face recognition error
        idname=['FACE RECOGNITION ERROR']         

    else:                                       # User is founded in the DB
        id_name=(r["person"]["FirstName"])      # Extracting the ID NAME from the json response
        id_lastname=(r["person"]["LastName"])
        idname=[(id_name+' '+id_lastname)]      # ID NAME
        id=(r['person']['UserID'])              # UserID NUMBER
        
        # OPEN LOCKER FUNCTIONS 
        lockerfree=checkLocker(id)                      # Getting LOCKER ID
        lockerO=lockerfree['LockerFree']['LockerID']    # Selecting LockerID
        hex_lock=literal_eval(lockerO)                  # Converting str to hex integer
        openflag=lockerfree['Openflag']                 # Getiing value Openflag 

        # When Openflag = 0: The USER Does not have any locker so automatically assign a Locker --> Option to Open locker
        # When Openflag = 1: Ther USER already have a locker so is able to :
        #       --> Option to Open locker and still using it 
        #       --> Option to Open locker and leave the laboratory 
        # Openflag is sent by a query from the API to the DB
        '''
        if openflag==0:                                 # This is cancelled but should activate or desactivate the buttons
            #OPEN LOCKER?
            '
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
                '''
        userIDs.append(idname)      #  When is appended the FOR is used but not neccesary because just one face will be detected     
    print("Reconocido!")


class CamApp(App):

    def build(self):
        self.img1=Image()       #For video
        self.btn1=Button(text='ABRIR LOCKER', font_size=30, size_hint=(0.33, .15), pos_hint={"x":0})                    # Button to open Locker
        self.btn2=Button(text='LIBERAR LOCKER', font_size=30, size_hint=(0.33, .15), pos_hint={"x":0.33, "bottom":1})   # Button to leave locker/building
        self.btn3=Button(text='CANCELAR', font_size=30, size_hint=(0.33, .15), pos_hint={"x":0.66, "bottom":1})         # Button to cancel the operation

        self.btn1.bind(on_press = self.OpenLocker)       # When btn1 pressed call function OpenLocker
        self.btn2.bind(on_press = self.SetFreeLocker)    # When btn1 pressed call function SetFreeLocker
        self.btn3.bind(on_press = self.Cancel)           # When btn1 pressed call function Cancel

        layout = FloatLayout()          # Defining the type of Layout to use
        layout.add_widget(self.img1)    #Adding the img1 (video)
        
        # Adding the 3 buttons (Are being showed on the screen)
        layout.add_widget(self.btn1)
        layout.add_widget(self.btn2)
        layout.add_widget(self.btn3)
        
        # Opencv2
        self.capture = cv2.VideoCapture(0)  # For camera in raspi
        cv2.namedWindow("CV2 Image")
        Clock.schedule_interval(self.update, 1.0/33.0)

        return layout

    def OpenLocker(self, event):        # Function - wheen "Abrir Locker" is pressed
        global hex_lock, lockerO, id    # Global variables updated in the THREAD 
        openLocker(hex_lock)            # Calling function to open the locker
        # updateDB (UserID, LockerID, leaveflag)  
        # leaveflag = 1 when the User will use again the locker
        updateDB(id, lockerO, 1)        # Updating the TALKE LockersUsers with UserID, LockerID, DATE, TIME
        print("User registered successfully") 
        

    def SetFreeLocker(self, event):     # Function - when "Liberar Locker" is pressed}
        global hex_lock, lockerO, id    # Global variables updated in the THREAD 
        openLocker(hex_lock)            # Calling function to open the locker
        # leaveflag = 2 when the User wont use again the locker (Leave the laboratory)
        updateDB(id, lockerO, 2)   # Updating the TABLE LockersUsers with UserID, LockerID, DATE, TIME
        
    def Cancel(self, event):            # Function - when "Cancelar" is pressed
        print("Has cancelado la operacion")

    def update(self, dt):

        global detectFace                       # Global variables updated in the THREAD 
        global idname, userIDs
        global y1,y2,x1,x2                      # This variables are global when the for is not used 

        ret, frame = self.capture.read()        # Inizialize camera and save frames in frame

        # THREADS

        frame = imutils.resize(frame, width=600)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # for haar cascade

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
        
        if len(faces) == 0:     # If there is any face detected
            rects = []
            idname = []
            detectFace = True   # Flag to
        
        if detectFace == True and len(faces) != 0:                  # A face is detected and detectFace is True
            encodings = face_recognition.face_encodings(rgb, rects) # Get encoding of detected faces
            
            x = threading.Thread(target=rec_function, args=(encodings,), daemon=True)   # Defining the THREAD for face recognition
            x.start()                                                                   # THREAD  started
            detectFace = False                                                          # After face recognition is finished
            
        if len(idname) > 0:                                             # If a face is recognized 
            # loop over the recognized faces (LOOP CANCELLED)
            finalid=idname[0]                                           # Getting the id from the vector
            cv2.rectangle(frame, (y2, x1), (y1, x2), (0, 255, 0), 2)    # Printing green rectangle in the face recognized
            y = x1 - 15 if x1 - 15 > 15 else x1 + 15
            cv2.putText(frame, finalid, (y2, y), cv2.FONT_HERSHEY_SIMPLEX,  # Printing name of the user 
                        0.5, (0, 255, 0), 2)
        else:                                                           # Printing red rectangle when the user is not recognized 
            for (x1, y1, x2, y2) in rects:
                # draw the predicted face id on the image
                cv2.rectangle(frame,(y2, x1), (y1, x2), ( 0, 255, 0), 2)
                
        cv2.imshow('Recognizer', frame)     # Show the frame (video)
        
        # To show the imshow(frame) on the UI
        # convert it to texture
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tobytes()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr') 
        #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.img1.texture = texture1

if __name__ == '__main__':
    CamApp().run()
    