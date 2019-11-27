import os
import numpy as np 
import cv2
import pickle
import sys
from Kpad import Keypad
from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image
import time

class Face_Recog_Op():
	def __init__(self):
		self.camera  = PiCamera()
		self.keypad = Keypad()
		self.camera.resolution = (640, 480)
		self.camera.framerate = 30
		self.rawCapture = PiRGBArray(self.camera, size=(640,480))
		self.faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

		self.recognizer = cv2.face.LBPHFaceRecognizer_create()
		if os.path.exists("trainer.yml"):
			print("등록된 얼굴을 불러옵니다.")
			self.recognizer.read("trainer.yml")
		else :
			print("등록된 얼굴이 없습니다!")
		
		if os.path.exists("labels"):
			with open('labels', 'rb') as f:
				self.dict = pickle.load(f)
			print("등록된 사용자 정보를 불러옵니다.")
		else :
			print("등록된 사용자가 없습니다.")

		self.baseDir = os.path.dirname(os.path.abspath(__file__))
		self.imageDir = os.path.join(self.baseDir, "images")
		self.currentId = 1
		self.labelIds = {}
		self.yLabels = []
		self.xTrain = []
		self.font = cv2.FONT_HERSHEY_SIMPLEX

	def add_face(self):
		print("키패드에서 A,B,C,D 중에서 눌러주세요")
		digit = None
		while digit == None:
			digit = self.keypad.getKey()
			if digit != None:
				name = str(digit)
				break
		
		dirName = "./images/_" + name
		print(dirName)
		if not os.path.exists(dirName):
			os.makedirs(dirName)
			print("Directory Created")
		else:
			print("Name already exists")
			# sys.exit()

		count = 1
		for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
			if count > 30:
				break
			frame = frame.array
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			faces = self.faceCascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
			for (x, y, w, h) in faces:
				roiGray = gray[y:y+h, x:x+w]
				fileName = dirName + "/" + name + str(count) + ".jpg"
				cv2.imwrite(fileName, roiGray)
				print (fileName,"저장됨")
				cv2.imshow("face", roiGray)
				cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
				count += 1

			cv2.imshow('frame', frame)
			key = cv2.waitKey(1)
			self.rawCapture.truncate(0)

			if key == 27:
				break

		cv2.destroyAllWindows()
	
	def train_faces(self):
		for root, dirs, files in os.walk(self.imageDir):
			print(root, dirs, files)
			for file in files:
				print(file)
				if file.endswith("png") or file.endswith("jpg"):
					path = os.path.join(root, file)
					label = os.path.basename(root)
					print(label)

					if not label in self.labelIds:
						self.labelIds[label] = self.currentId
						print(self.labelIds)
						self.currentId += 1

					id_ = self.labelIds[label]
					pilImage = Image.open(path).convert("L")
					imageArray = np.array(pilImage, "uint8")
					faces = self.faceCascade.detectMultiScale(imageArray, scaleFactor=1.1, minNeighbors=5)

					for (x, y, w, h) in faces:
						roi = imageArray[y:y+h, x:x+w]
						self.xTrain.append(roi)
						self.yLabels.append(id_)

		with open("labels", "wb") as f:
			pickle.dump(self.labelIds, f)

		self.recognizer.train(self.xTrain, np.array(self.yLabels))
		self.recognizer.save("trainer.yml")
		print(self.labelIds)
		print("얼굴 트레이닝 완료")

	def detect_face(self):
		start = time.time()
		for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
			frame = frame.array
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			faces = self.faceCascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
			for (x, y, w, h) in faces:
				roiGray = gray[y:y+h, x:x+w]

				id_, conf = self.recognizer.predict(roiGray)

				for name, value in self.dict.items():
					if value == id_:
						print(name)
						cv2.destroyAllWindows()
						return name     
				if conf <= 70:
					cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
					cv2.putText(frame, name + str(conf), (x, y), self.font, 2, (0, 0 ,255), 2,cv2.LINE_AA)
			
			#시간 초과
			if (time.time() - start) >= 10:
				return -1

			cv2.imshow('frame', frame)
			key = cv2.waitKey(1)

			self.rawCapture.truncate(0)

			if key == 27:
				break

		cv2.destroyAllWindows()


if __name__ == '__main__':
	a = Face_Recog_Op()
	a.add_face()
	# a.train_faces()
	# a.detect_face()
