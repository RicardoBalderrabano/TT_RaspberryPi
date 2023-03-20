from smbus import SMBus
from itertools import cycle
from time import sleep


bus = SMBus(1) # Port 1 used on REV2 

bus.write_byte(0x38,0x00)   #Salidas en 0
sleep(1)                    #Tiempo de espera 1s
bus.write_byte(0x38,0x01)   #P0 en 1
sleep(1)                    #Tiempo de espera 1s
bus.write_byte(0x38,0x00)   #Salidas en 0
sleep(3)                    #Tiempo de espera 3s
bus.write_byte(0x38,0x04)   #P3 en 1
sleep(1)                    #Tiempo de espera 1s
bus.write_byte(0x38,0x00)   #Salidas en 0
sleep(3)                    #Tiempo de espera 3s
bus.write_byte(0x38,0x10)   #P5 en 1
sleep(1)                    #Tiempo de espera 1s
bus.write_byte(0x38,0x00)   #Salidas en 0
sleep(1)                    #Tiempo de espera 1s
