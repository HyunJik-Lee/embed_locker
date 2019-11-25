from ServoMotor import Motor
from Dot import Dot
from Kpad import Keypad
from TactSwitch import TactSwitch
from LimitSwitch import LimitSwitch
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class Locker():
    def __init__(self):
        self.dot = Dot()
        self.keypad = Keypad()
        self.motor = Motor()
        self.lock_switch = 19
        self.change_pass_switch = 13
        self.close_switch = 5
        self.Locked = True
        self.Door_closed = True
        self.passwd = [1,2,3,4,'#']
        GPIO.setup(19, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(13, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(5, GPIO.IN, GPIO.PUD_UP)
        GPIO.add_event_detect(19, GPIO.RISING, callback = self.door_op, bouncetime=2000)
        GPIO.add_event_detect(13, GPIO.RISING, callback = self.change_passwd_op, bouncetime = 10000)

    def door_op(self, channel):
        if self.Locked is True:
            self.motor.turn180(False, 0.2)
            self.dot.unlock()
            self.Locked = False
            return

        if self.Locked is False:
            self.motor.turn180(True, 0.2)
            self.dot.lock()
            self.Locked = True
            return

    def pw_door_open(self):
        seq = []
        i = 0
        print('비밀번호 입력, 초기화는 \'D\', 취소는 \'C\'')
        while i != len(self.passwd):
            digit = None
            while digit == None:
                digit = self.keypad.getKey()
                if digit != None:
                    if digit == 'D':
                        seq.clear()
                        print('초기화')
                        i = 0
                    elif digit == 'C':
                        print('취소')
                        return
                    else:
                        print(digit)
                        i = i + 1
                        seq.append(digit)
            time.sleep(0.4)

        print(seq)

        if seq == self.passwd:
            self.door_op(True)
            print('문이 열립니다.')
            return
        else:
            self.dot.fail()
            print('비밀번호가 틀렸습니다.')
            return

    def change_passwd_op(self, channel):
        seq = []
        print('변경할 비밀번호 입력후 \'#\' 입력, 초기화는 \'D\', 취소는 \'C\'')
        digit = None
        while digit == None:
            digit = self.keypad.getKey()
            if digit != None:
                if digit == 'D':
                    seq.clear()
                    print('초기화')
                    digit = None
                elif digit == 'C':
                    print('취소')
                    return
                elif digit != '#':
                    seq.append(digit)
                    print(digit)
                    digit = None
                elif digit == '#':
                    self.passwd = seq
                    print('변경완료')
                    return
            time.sleep(0.4)
    
    def face_recognization(self):
        pass


if __name__ == '__main__':
    a = Locker()
    while True:
        digit = None
        while digit == None:
            digit = a.keypad.getKey()
            if digit == '*':
                time.sleep(0.4)
                a.pw_door_open()
                digit = None


        if GPIO.event_detected(19):
            print('Tact 19 Pressed')
        if GPIO.event_detected(13):
            print('Tact 13 Pressed')
    

