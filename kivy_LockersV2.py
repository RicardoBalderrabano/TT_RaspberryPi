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
# Buttons pressed 2 times
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
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

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
IDlocker='0'
buttonsFlag=0



class CamApp(App):

    def build(self):

        self.img1=Image()       #For video
        self.btn1=Button(text='REGISTRAR', font_size=30, size_hint=(1,.18), pos_hint={"x":0, "bottom":1}, opacity=1, disabled= False)  # Button to do registration
        
        self.btn1.bind(on_release = self.rec_function)       # When btn1 pressed call function OpenLocker

        #layout = FloatLayout()          # Defining the type of Layout to use
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.img1)    #Adding the img1 (video)
        
        # Adding the button (Shows on the screen)
        layout.add_widget(self.btn1)
        
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

    global IDlocker  

    
    def ThreadOpenLockers(self, event):     # Function for OpenLockerThread when btn1 is pressed 
        global popup2, popup
        thLo = threading.Thread(target=self.OpenLocker, args=(event,)).start()   # Defining the THREAD for OpenLocker}
        
        layout = GridLayout(cols = 1, padding = 10)
        

        popupLabel = Label(text = "LOCKER " + IDlocker + " HA SIDO ABIERTO")
        closeButton = Button(text = "OK", font_size=30, size_hint_y=None, height=80)
  
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)  
  
        # Instantiate the modal popup and display
        popup = Popup(title ='Aviso',
                      content = layout,
                      size_hint =(None, None), size =(400, 400))  
        popup.open()   
  
        # Attach close button press with popup.dismiss action
        closeButton.bind(on_press = popup.dismiss)
        closeButton.bind(on_press = popup2.dismiss)


    def SetFreeLocker(self, event):     # Function - when "Liberar Locker" is pressed}
        global hex_lock, lockerO, id    # Global variables updated in the THREAD 
        openLocker(hex_lock)            # Calling function to open the locker
        # leaveflag = 2 when the User wont use again the locker (Leave the laboratory)
        updateDB(id, lockerO, 2)   # Updating the TABLE LockersUsers with UserID, LockerID, DATE, TIME

    def ThreadSetFreeLocker(self, event):     # Function for SetLockerThread when btn1 is pressed 
        thFreeLo = threading.Thread(target=self.SetFreeLocker, args=(event,)).start()   # Defining the THREAD for SetFreeLocker      
        
        layout = GridLayout(cols = 1, padding = 10)

        popupLabel = Label(text = "LOCKER " + IDlocker + " HA SIDO LIBERADO")
        closeButton = Button(text = "OK", font_size=30, size_hint_y=None, height=80)
  
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)  
  
        # Instantiate the modal popup and display
        popup = Popup(title ='Aviso',
                      content = layout,
                      size_hint =(None, None), size =(400, 400))  
        popup.open()   
  
        # Attach close button press with popup.dismiss action
        closeButton.bind(on_press = popup.dismiss)
        closeButton.bind(on_press = popup2.dismiss)

    def Cancel(self, event):            # Function - when "Cancelar" is pressed
        print("Has cancelado la operacion")       

    def ThreadCancel(self, event):
        thCancel=threading.Thread(target=self.Cancel, args=(event,)).start()

    def rec_function(self, event):
        global rects, rgb, idname, popup2, lockerO, id, hex_lock
        closeButton = Button(text = "CANCELAR", font_size=30, size_hint_y=None, height=80)
        self.btn1=Button(text='ABRIR LOCKER', font_size=30, size_hint_y=None, height=80)                    # Button to open Locker
        self.btn2=Button(text='LIBERAR LOCKER', font_size=30, size_hint_y=None, height=80)   # Button to leave locker/building
        layout = GridLayout(cols = 1, padding = 10)

        encodings = face_recognition.face_encodings(rgb, rects) # Get encoding of detected faces
        print("Reconociendo...")

        # Sending encodings and getting ID
        r=send_encodingsLockers(URL_SERVER,PAGE,encodings)

        res= r['message'] # Checking the response in the JSON 

        # Is the user found? 
        if res=='UserNoFound':                  # User no founded
            idname='Usuario no encontrado en la base de datos. \n Dirigirse con el administrador.'    # ID NAME 
            
        elif res=='FACE RECOGNITION ERROR':     # Face recognition error
            idname='Error en el reconocimiento facial. Presione OK y vuelva a intentarlo.'       

        else:                                       # User is founded in the DB
        
            id_name=(r["person"]["FirstName"])      # Extracting the ID NAME from the json response
            id_lastname=(r["person"]["LastName"])
            idname1=[(id_name+' '+id_lastname)]      # ID NAME
            #idname='REGISTRO EXITOSO ' + idname1[0]
            id=(r['person']['UserID'])              # UserID NUMBER
            idname=idname1[0]
            # OPEN LOCKER FUNCTIONS 
            lockerfree=checkLocker(id)                      # Getting LOCKER ID
            lockerO=lockerfree['LockerFree']['LockerID']    # Selecting LockerID
            IDlocker=str(lockerfree['LockerFree']['DirectionF']) # Locker number
            print(lockerO)
            print(lockerfree)
            hex_lock=literal_eval(lockerO)                  # Converting str to hex integer
            openflag=lockerfree['Openflag']                 # Getiing value Openflag 

            # When Openflag = 0: The USER Does not have any locker so automatically assign a Locker --> Option to Open locker
            # When Openflag = 1: Ther USER already have a locker so is able to :
            #       --> Option to Open locker and still using it 
            #       --> Option to Open locker and leave the laboratory 
            # Openflag is sent by a query from the API to the DB
            print(openflag)
            if openflag==0:
                # ENABLE 2 BUTTONS

                popupLabel = Label(text = idname)


                layout.add_widget(popupLabel)
                layout.add_widget(closeButton) 
                layout.add_widget(self.btn1) 
        
                # Instantiate the modal popup and display
                popup2 = Popup(title ='Aviso',
                            content = layout,
                            size_hint =(None, None), size =(800, 600))  
                popup2.open()   
        
                # Attach close button press with popup.dismiss action
                closeButton.bind(on_press = popup2.dismiss)
                self.btn1.bind(on_release = self.ThreadOpenLockers)       # When btn1 pressed call function OpenLocker
            
            else:
                # ENABLE 3 BUTTONS

                popupLabel = Label(text = idname)

                layout.add_widget(popupLabel)
                layout.add_widget(closeButton) 
                layout.add_widget(self.btn1) 
                layout.add_widget(self.btn2)
 
        
                # Instantiate the modal popup and display
                popup2 = Popup(title ='Aviso',
                            content = layout,
                            size_hint =(None, None), size =(400, 400))  
                popup2.open()   
        
                # Attach close button press with popup.dismiss action
                closeButton.bind(on_press = popup.dismiss)
                self.btn1.bind(on_release = self.ThreadOpenLockers)       # When btn1 pressed call function OpenLocker
                self.btn2.bind(on_release = self.ThreadSetFreeLocker)    # When btn1 pressed call function SetFreeLocker

    def update(self, dt):

        global rects, rgb
        rects = []
        ret, frame = self.capture.read()        # Inizialize camera and save frames in frame

        frame = imutils.resize(frame, width=900)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # for haar cascade

        # Detect face using haar cascades
        faces = face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.3, 
            minNeighbors=5,
            minSize=(190,190))  # Modify the distance to detect a face

        # convert bounding boxes (x, y, w, h) to face locations in css (top, right, bottom, left) order
        for (x,y,w,h) in faces:
            rects.append([y, x+w, y+h, x])
        
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
    