from ServoMotor import Motor
from Dot import Dot
from Kpad import Keypad
from TactSwitch import TactSwitch
from LimitSwitch import LimitSwitch
import time
import RPi.GPIO as GPIO

passwd = [1,2,3,'#']

def door_op(Locked):
    if Locked is True:
        motor.turn180(False, 0.2)
        dot.unlock()
        
    if Locked is False:
        motor.turn180(True, 0.2)
        dot.lock()

    
def pw_door_open(keypad):
    seq = []
    i = 0
    print('비밀번호 입력')
    while i != len(passwd):
        digit = None
        while digit == None:
            digit = keypad.getKey()
            if (digit != None):
                if(digit == 'D'):
                    seq.clear()
                    print('초기화')
                    i = 0
                else:
                    print(digit)
                    i = i + 1
                    seq.append(digit)
                    
        time.sleep(0.4)
    if seq == passwd:
        door_op(True)
    else:
        door_op(False)
    

def change_passwd_op(keypad):
    global passwd
    passwd.clear()
    print('변경할 비밀번호 입력후 \'#\' 입력, 초기화는 \'D\'')
    digit = None
    while digit == None:
        digit = keypad.getKey()
        if (digit != None):
            if digit == 'D':
                passwd.clear()
                print('초기화')
                digit = None
                
            elif(digit != '#'):
                passwd.append(digit)
                print(digit)
                digit = None
            
        time.sleep(0.4)


def face_recognization():
    pass

if __name__ == '__main__':
    dot = Dot()
    keypad = Keypad()
    motor = Motor()
    lock_switch = TactSwitch(19)
    change_pass_switch = TactSwitch(13)
#    limit_switch = LimitSwitch(5)
    Locked = True
    door_closed = True # limit_switch.isPushed()
    ltime = 0
    GPIO.setup(5, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(19, GPIO.RISING, callback=lambda x : door_op(Locked), bouncetime=2000)

    while True:
        if GPIO.event_detected(19):
            print('Tact 19 Pressed')
            Locked = not Locked
#     change_passwd_op(keypad)
    
#    temp = None
#    while temp == None:
#        temp = keypad.getKey()
#        if temp == '*':
#            time.sleep(1)
#            pw_door_open(keypad)
#        elif temp == 'B':
#            time.sleep(1)
#            change_passwd_op(keypad)
        
        
    motor.clear()

#     while True:
#         if tact.isClicked():
#             Locked = door_op(Locked)
#  아무래도 쓰레드로 구현 해야 할것 같습니다만..
#         if not Locked:
#             time.sleep(3)
#             if
#             motor.turn180(True, 0.2)
#             dot.lock()
#             Locked = True
#         elif Locked is False:
#             time.sleep(3)
#             motor.turn180(True, 0.2)
#             dot.lock()
#             Locked = not Locked
        
