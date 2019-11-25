import RPi.GPIO as GPIO
import time

class TactSwitch:
    def __init__(self, tact_pin =19):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(tact_pin, GPIO.IN, GPIO.PUD_UP)
        self.tact = tact_pin
        
    def isClicked(self):
        while True:
            temp = GPIO.input(self.tact)
            if temp == 0:
                return True

if __name__ == '__main__':
    swi = TactSwitch()
    if swi.isClicked():
        print('clicked')
    

