#This is the connection with the server. It is used the library "request" to make a POST in the server.
#The POST includes the ENCODINGS obtained from the "test_reconizerViolaEncodings.py" in the Raspberry Pi.
import requests

#Server information 
URL_SERVER = 'http://140.84.179.17:80'
PAGE = "/encodings"

'''
def data_encodings(array_encodings):
    data={'encodings': array_encodings}
    return data    '''
    
def send_encodings(URL_SERVER, PAGE, array_encodings):
    dataE={'encodings': array_encodings}
    requests.post(URL_SERVER+PAGE,dataE)
    return 



#print(f"Response: {r.json()}")