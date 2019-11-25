from ServoMotor import Motor
from Dot import Dot
from Kpad import Keypad
import time
import RPi.GPIO as GPIO
import Locker
passwd = [1,2,3,4,'#']

dot = Dot()
keypad = Keypad()
motor = Motor()

door_op(True)
door_op(False)
