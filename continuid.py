import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
servo_pin=18
button_pin=23

GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

servo=GPIO.PWM(servo_pin,50)
servo. start(0)

while True:
    input_state = GPIO.input(button_pin)
    print(input_state)
    if input_state== False:
        for angle in range(0,181,1):
            duty_cycle=2+(angle/18)
            servo.ChangeDutyCycle(duty_cycle)
            sleep(0.01)
            
            
    while GPIO.input(button_pin)== False:
        pass
    
    
    for angle in range(180,-1,-1):
        duty_cycle=2+(angle/18)
        servo.ChangeDutyCycle(duty_cycle)
        sleep(0.01)
        
        
    while GPIO.input(button_pin)==False:
        pass
    
    
servo.stop()
GPIO.cleanup()