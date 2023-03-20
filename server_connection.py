#This is the connection with the server. It is used the library "request" to make a POST in the server.
#The POST includes the ENCODINGS obtained from the "test_reconizerViolaEncodings.py" in the Raspberry Pi.
#import requests
from flask import jsonify
import requests
import numpy as np
import json
from json import JSONEncoder

#Server information 
URL_SERVER = 'http://140.84.179.17:80'
PAGE = "/encodings"

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def send_encodings(URL_SERVER,PAGE,arrayEncoding):
    numpyData={"encoding":arrayEncoding}
    encodedNumpyData=json.dumps(arrayEncoding,cls=NumpyArrayEncoder)
    msg={"encoding":encodedNumpyData}
    r = requests.post(URL_SERVER+PAGE,json=msg)
    return 

