import RPi.GPIO as GPIO
import time

class Motor:
    #모터 핀을 초기화할 때 정할 수 있다.
    def __init__(self, mot_pin=26):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(mot_pin, GPIO.OUT)
        self.Mot = GPIO.PWM(26, 50)
        self.Mot.start(0)
    
    def turn180(self, isLock, delay=2):
        if isLock == True:
            self.Mot.ChangeDutyCycle(12)
            time.sleep(delay)
            return
        
        elif isLock == False:
            self.Mot.ChangeDutyCycle(2)
            time.sleep(delay)
            return
        
    def clear(self):
        self.Mot.stop()
        GPIO.cleanup()
        
        
if __name__ == '__main__':
    motor = Motor()
    #모터의 초기 상태는 잠금해제 되어 있다.
    motor.turn180(True)
    motor.turn180(False)
    motor.clear()