'''
In this example the Encoding is serialized into JSON String and POST it to the server
'''
import requests
import json
from json import JSONEncoder
import numpy as np
from flask import jsonify # <- `jsonify` instead of `json`
from server_connection import send_encodings


#SERVER
URL_SERVER = 'http://140.84.179.17:80'
PAGE = "/encodings"

#encoding example
arr=np.array([-0.16204873,  0.05700064,  0.09044103, -0.0289933,  0.0105991, -0.06313304,  0.02532312, -0.06310672,  0.19280991, -0.06976435,0.27877778, -0.02801619, -0.16462296, -0.08764254,  0.0184108 ,0.10018795, -0.1614228 , -0.07778311, -0.05854391, -0.09281124,0.03796965, -0.06505482,  0.08574302,  0.08136091, -0.13039035,-0.33689976, -0.12185112, -0.17633946,  0.04835968, -0.12887856, 0.03734888, -0.03419122, -0.13015796, -0.01792823, -0.09167993, 0.01533425, -0.01064435, -0.09707557,  0.22708979, -0.05149043, -0.08824956, -0.06267489, -0.01708418,  0.23643188,  0.16007985, -0.01498417,  0.02098352, -0.02181685,  0.11432847, -0.18134783, 0.08841863,  0.07719498,  0.08711237,  0.04825372,  0.09451386, -0.04723743,  0.03988895,  0.07965464, -0.18946315,  0.07275526, 0.04725489,  0.00468429, -0.05424148,  0.00258533,  0.21708301, 0.13386893, -0.10268205, -0.11519437,  0.12464185, -0.11972477, 0.0076764 ,  0.07027947, -0.14508457, -0.18435466, -0.2220473 , 0.10926897,  0.35384247,  0.08600141, -0.14343464, -0.00359992, -0.12797044, -0.04468407,  0.0458146 , -0.00036053, -0.1260138 , -0.01638346, -0.13420668,  0.06053462,  0.13769779,  0.01063394, -0.06730839,  0.21319255, -0.03024589, -0.00797784,  0.03337118, 0.03299601, -0.07148667,  0.05303938, -0.08697553,  0.02529288, 0.14805099, -0.06713539, -0.01860933,  0.03342337, -0.16720949, 0.09504434,  0.00657883, -0.00571885,  0.03074568,  0.04273393,-0.23216605, -0.05640813,  0.16825019, -0.22020227,  0.15109515,0.13512151,  0.07386337,  0.10670583,  0.05183314,  0.06663342,-0.01184203,  0.01027293, -0.10881106,  0.03098165,  0.07032161,0.01464648,  0.03970058,  0.03728874])
lista=[(arr)]
encodings=lista

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
    return print(f"Response: {r.json()}")


send_encodings(URL_SERVER,PAGE,encodings)
#print(r)
'''
if r.status_code != 200:
  print ("Error:", r.status_code)'''





