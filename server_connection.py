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

