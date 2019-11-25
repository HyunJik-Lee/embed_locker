import RPi.GPIO as GPIO
import time

class LimitSwitch:
    def __init__(self, limit_pin=5):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(limit_pin, GPIO.IN, GPIO.PUD_UP)
        self.limit = limit_pin
        
    def isPushed(self):
        while True:
            temp = GPIO.input(self.limit)
            if temp == 1:
                return True
            elif temp == 0:
                return False

if __name__ == '__main__':
    swi = LimitSwitch()
    while True:
        if swi.isPushed():
            print('Pushed')