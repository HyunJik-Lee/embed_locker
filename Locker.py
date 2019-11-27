from ServoMotor import Motor
from Dot import Dot
from Kpad import Keypad
from TactSwitch import TactSwitch
from LimitSwitch import LimitSwitch
from FaceRecognition import Face_Recog_Op
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class Locker():
	def __init__(self):
		self.dot = Dot()
		self.keypad = Keypad()
		self.motor = Motor()
		self.face_recog_op = Face_Recog_Op()
		self.lock_switch = 19
		self.change_pass_switch = 13
		self.close_switch = 5
		self.add_face_switch = 6
		self.Locked = True
		self.Door_closed = True
		self.passwd = [1,2,3,4,'#']
		GPIO.setup(self.lock_switch, GPIO.IN, GPIO.PUD_UP)
		GPIO.setup(self.change_pass_switch, GPIO.IN, GPIO.PUD_UP)
		GPIO.setup(self.close_switch, GPIO.IN, GPIO.PUD_UP)
		GPIO.setup(self.add_face_switch, GPIO.IN, GPIO.PUD_UP)
		GPIO.add_event_detect(self.lock_switch, GPIO.RISING, callback = self.door_op, bouncetime=2000)
		GPIO.add_event_detect(self.change_pass_switch, GPIO.RISING, callback = self.change_passwd_op, bouncetime = 10000)
		GPIO.add_event_detect(self.close_switch, GPIO.RISING, callback = self.close_after_3s, bouncetime = 5000)
		GPIO.add_event_detect(self.add_face_switch, GPIO.RISING, callback = self.face_add_and_train, bouncetime = 100000)

	def close_after_3s(self, channel):
		print('문이 닫혔습니다.')
		time.sleep(3)
		if GPIO.input(self.close_switch) is 1 and self.Locked is False :
			print('문을 잠급니다.')
			self.door_op(True)


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
			self.dot.success()
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
	
	def face_door_open(self):
		print("얼굴 인식 중입니다. 카메라를 응시해 주세요.")
		self.dot.smile()
		name = self.face_recog_op.detect_face()
		if name in self.face_recog_op.dict:
			self.dot.success()
			self.door_op(True)
			return
		else:
			self.dot.fail()
			print('인식에 실패했거나 등록되지 않은 얼굴입니다.')
			return

	def face_add_and_train(self, channel):
		print("얼굴 추가 중입니다. 카메라를 응시해 주세요.")
		self.dot.question()
		self.face_recog_op.add_face()
		self.dot.question()
		self.face_recog_op.train_face()
		self.dot.success()
		print("추가 완료")
		return

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
			if digit == '#':
				time.sleep(0.4)
				a.face_door_open()
				digit = None
		
		if GPIO.event_detected(a.lock_switch):
			print('Tact 19(lock_switch) Pressed')
		if GPIO.event_detected(a.change_pass_switch):
			print('Tact 13(change_pass_switch) Pressed')
		if GPIO.event_detected(a.add_face_switch):
			print('Tact 6(add_face_switch) Pressed')
	

