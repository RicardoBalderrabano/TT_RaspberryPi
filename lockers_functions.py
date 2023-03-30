'''
This script contains the functions used in the Raspberry_Lockers.py file.
'''
from smbus import SMBus
from itertools import cycle
from time import sleep
from server_connection import getLockers

bus = SMBus(1) # Port 1 used on REV2 (I2C Configuration)

# OPEN LOCKER FUNCTION 
def openLocker(lockerID): # Getting the Locker direction
    bus.write_byte(0x38,lockerID) # Sending HIGH to the direction (1 second)
    sleep(1)
    bus.write_byte(0x38,0x00)   # Sending LOW for all the directions
    sleep(3)                    
    return
'''
#FUNCTION TO GET THE SATUS OF THE LOCKERS 
def getStatusLockers(userID):
    res=getLockers(userID)
    locker=res['LockerFree']
    return jasonify(locker)

'''

