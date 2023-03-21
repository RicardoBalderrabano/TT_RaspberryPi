# TT_RaspberryPi
This repository contains the codes for the Trabajo Terminal used in the raspberry.

The Trabajo Terminal consists in the access control to the laboratories of the building "Edificio de laboratorios de Pesados" of the UPIITA. 

Here are described the documents of the repository:

**haarcascade_frontalface_default.xml
      --This file contains the information for the training ViolaJones-HaarCascade algorithm used in "test_reconizerViolaEncodings.py"
      
**test_reconizerViolaEncodings.py
    --This file makes the connection with the camera connected to the raspberry pi to detect the faces with ViolaJones algorithm and use de faces_recognition library to       obtain the 128 vector of the face detected and send the information using a request post to the server.
    
**server_connection.py 
    --This file contains the function to send the information to the server using the library request.
