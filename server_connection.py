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

# FUNCTION TO SEND ENCODING AND GET ID FROM THE DB ---> route(/encodings)
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

# FUNCTION FOR RASPBERRY LOCKERS ---> route(/encodings)
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

# GET ALL LOCKERS REGISTERED FUNCTION ---> NO USED
def getLockers(UserID):
    status_direc='/Lockers_Status' # Direction for API
    msg={'UserID': UserID} #Sending UserID
    r=requests.post(URL_SERVER+status_direc, json=msg) # POST 
    return r.json() # Getting lockers registered and Locker ID/Direction to be opened

# CHECK IF THE USER HAS ALREADY A LOCKER ---> route(/CheckLocker)
# Returns the LockerID :
# When the user has already a locker or assigs a new locker
def checkLocker(UserID):
    checkLo='/CheckLocker'
    msg={'UserID':UserID} # Sending UserID
    r=requests.post(URL_SERVER+checkLo, json=msg) # POST 
    return r.json() # Getting lockers registered and Locker ID/Direction to be opened

# UPDATE DB FUNCTION ---> route(/updateRegister)
# leaveflag is 1 when the user will use the locker again, 2 when the user leaves the Building
def updateDB(UserID, LockerID, leaveflag): # Getting UserID, LockerID to be registered and leaveflag 
    update_direc='/updateRegister' # Direction for API
    UserID_Str=UserID   # UserID
    LeaveFlag=leaveflag # leaveflag 
    msg={'UserID':UserID_Str, 'LockerID': LockerID, 'Leaveflag': LeaveFlag} # UserID, LockerID and leaveflag Message (JSON) 
    R=requests.post(URL_SERVER+update_direc,json=msg) # POST to the direction
    return 

# INSERT DB FOR LABORATORIES ---> route(/registrationL)
# Send the UserIID, LaboratoryID 
def updateDB_Laboratory(UserID, LaboratoryID):
    update_direc='/registrationL' 
    msg={'UserID': UserID, 'LaboratoryID':LaboratoryID}
    R=requests.post(URL_SERVER+update_direc, json=msg)  
    return R.json()     # Registration done message / ACCESO NEGADO 
'''
resInser=updateDB_Laboratory(1,1)  # LaboratoryID
print(resInser)'''