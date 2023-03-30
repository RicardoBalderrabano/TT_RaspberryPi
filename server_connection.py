#This is the connection with the server. It is used the library "request" to make a POST in the server.
#The POST includes the ENCODINGS obtained from the "test_reconizerViolaEncodings.py" in the Raspberry Pi.
#import requests
from flask import jsonify
import requests
import numpy as np
import json
from json import JSONEncoder

# Server INFORMATION 
URL_SERVER = 'http://140.84.179.17:80'
PAGE = "/encodings"
LOCKERS="/Lockers"

# CLASS FOR SERIALIZATION OF THE ENCODINGS
class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

# FUNCTION TO SEND ENCODING AND GET ID FROM THE DB
def send_encodings(URL_SERVER,PAGE,Encoding):

    if not Encoding:        # For empty encoding
        arrayEncoding=[0]   # Select array to send
    else:
        arrayEncoding=Encoding[0]   # Select array to send

    numpyData={"encoding":arrayEncoding}    
    encodedNumpyData=json.dumps(arrayEncoding,cls=NumpyArrayEncoder) # Serialization
    msg={"encoding":encodedNumpyData}       # Message to send in JSON
    r = requests.post(URL_SERVER+PAGE,json=msg)     # POST TO API (SERVER)
    return r.json()     # Response ID   

# FUNCTION FOR RASPBERRY LOCKERS
def send_encodingsLockers(URL_SERVER, PAGE, Encoding):
    
    if not Encoding:        # For empty encoding
        arrayEncoding=[0]   # Select array to send
        #return jsonify({'message':'UserNoFound'})
    else:
        arrayEncoding=Encoding[0]   # Select array to send

    numpyData={"encoding":arrayEncoding}    
    encodedNumpyData=json.dumps(arrayEncoding,cls=NumpyArrayEncoder) # Serialization
    msg={"encoding":encodedNumpyData}       # Message to send in JSON
    r = requests.post(URL_SERVER+PAGE+LOCKERS,json=msg)     # POST TO API (SERVER)
    return r.json()     # Response ID   

# GET ALL LOCKERS REGISTERED FUNCTION
def getLockers(UserID):
    status_direc='/Lockers_Status' # Direction for API
    msg={'UserID': UserID} #Sending UserID
    r=requests.post(URL_SERVER+status_direc, json=msg) # POST 
    return r.json() # Getting lockers registered and Locker ID/Direction to be opened

# CHECK IF THE USER HAS ALREADY A LOCKER
def checkLocker(UserID):
    checkLo='/CheckLocker'
    msg={'UserID':UserID} # Sending UserID
    r=requests.post(URL_SERVER+checkLo, json=msg) # POST 
    return r.json() # Getting lockers registered and Locker ID/Direction to be opened

# UPDATE DB FUNCTION 
def updateDB(UserID, LockerID, leaveflag): # Getting UserID and LockerID to be registered 
    update_direc='/updateRegister' # Direction for API
    UserID_Str=UserID # Convert int to str (UserID)
    LeaveFlag=leaveflag
    msg={'UserID':UserID_Str, 'LockerID': LockerID, 'Leaveflag': LeaveFlag} # UserID and LockerID Message (JSON) 
    R=requests.post(URL_SERVER+update_direc,json=msg) # POST to the direction
    return 
'''
UserID=1
DIRE='0x01'
r=updateDB(UserID, DIRE,1)
print(r)'''