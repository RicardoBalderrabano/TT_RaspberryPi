'''
import RPi.GPIO as  GPIO
GPIO.setmode(GPIO.BCM) 
GPIO.setup(17, GPIO.OUT) 
GPIO.output(17, False)
'''
import RPi.GPIO as GPIO
''' 
# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
 
# set up the GPIO channels - one input and one output
GPIO.setup(27, GPIO.IN)
GPIO.setup(17, GPIO.OUT)
 
# input from pin 27
input_value = GPIO.input(27)
 
# output to pin 12
GPIO.output(17, GPIO.HIGH)
'''

 
# the same script as above but using BCM GPIO 00..nn numbers
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN)
GPIO.setup(17, GPIO.OUT)

GPIO.output(17, GPIO.LOW)
input_value = GPIO.input(27)

print(input_value)