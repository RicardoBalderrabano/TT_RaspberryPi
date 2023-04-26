# This script has an example of a GUI to use in the raspberry pi
# Make the facial detection and print the name "Ricardo" when a face is detected
# Has 3 buttons but just btn1 has a function to print a text when is pressed
# To use run on raspberry pi first run "export DISPLAY=:0"


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
import cv2
from kivy.uix.floatlayout import FloatLayout

import imutils

# Load haar cascade file
#haarCascade = 'D:\\RICARDO\\Escritorio\\upiita\\SEMESTRE 10\\TT2\\RasberryPi codes\\TT_RaspberryPi\\haarcascade_frontalface_default.xml'  
haarCascade = '/home/ricardo/TT_tests/haarcascade_frontalface_default.xml'  #for raspi

face_cascade = cv2.CascadeClassifier(haarCascade)


class CamApp(App):

    def build(self):
        self.img1=Image()
        self.btn1=Button(text='ABRIR LOCKER', font_size=30, size_hint=(0.33, .15), pos_hint={"x":0})
        self.btn2=Button(text='LIBERAR LOCKER', font_size=30, size_hint=(0.33, .15), pos_hint={"x":0.33, "bottom":1})
        self.btn3=Button(text='CANCELAR', font_size=30, size_hint=(0.33, .15), pos_hint={"x":0.66, "bottom":1})

        self.btn1.bind(on_release = self.callback)

        layout = FloatLayout()
        layout.add_widget(self.img1)
       
        layout.add_widget(self.btn1)
        layout.add_widget(self.btn2)
        layout.add_widget(self.btn3)
        
        #opencv2 stuffs
        self.capture = cv2.VideoCapture(0)
        cv2.namedWindow("CV2 Image")
        Clock.schedule_interval(self.update, 1.0/33.0)

        return layout

    def callback(self, event):
        print("button pressed")
        print('Yoooo !!!!!!!!!!!') 
        

    def update(self, dt):

        #Face detected flag
        face_detected=False

        # display image from cam in opencv window
        ret, frame = self.capture.read()
        #cv2.imshow("CV2 Image", frame)
        frame = imutils.resize(frame, width=600)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # For haar cascade

        # Detect face using haar cascades
        faces = face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.3, 
            minNeighbors=5,
            minSize=(190,190))  # Modify the distance to detect a face

        if len(faces)>0:
            face_detected=True
            rects = []
            # Convert bounding boxes (x, y, w, h) to face locations in css (top, right, bottom, left) order
            for (x,y,w,h) in faces:
                rects.append([y, x+w, y+h, x])
            idname=[('Ricardo')]
                # Loop over the recognized faces
            for ((x1, y1, x2, y2), idname) in zip(rects,idname):
                # draw the predicted face id on the image
                cv2.rectangle(frame, (y2, x1), (y1, x2), (0, 255, 0), 2)
                y = x1 - 15 if x1 - 15 > 15 else x1 + 15
                cv2.putText(frame, idname, (y2, y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 255, 0), 2)

            cv2.imshow('Recognizer', frame)
        
        else:
            cv2.imshow("CV2 Image", frame)

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
    #cv2.destroyAllWindows()