import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

class Keypad:
    #키패드의 행과 열의 핀번호를 리스트로 전달하여 초기화 할 수 있다.
    def __init__(self, row_pin=[18,23,24,25], col_pin=[4,17,22,21]):
        GPIO.setmode(GPIO.BCM)
        self.KEYPAD = [
                [1,2,3,"A"],
                [4,5,6,"B"],
                [7,8,9,"C"],
                ["*",0,"#","D"]
                ]
        self.ROW = row_pin
        self.COLUMN = col_pin
        self.use = "main"
        
    def getKey(self):
        #모든 열을 output으로 설정
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)
            
        #모든 행을 input으로 설정
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, GPIO.PUD_UP)
            
        #눌려진 행을 찾는 반복문, rowNum은 0~3의 값만 가질 수 있음
        rowNum = -1
        for i in range(len(self.ROW)):
            tmp = GPIO.input(self.ROW[i])
            if tmp == 0:
                rowNum = i
                 
        # rowNum이 0보다 작거나 3보다 큰 경우 눌린 것이 없다고 판단
        if rowNum < 0 or rowNum > 3:
            self.clear()
            return None
         
        # 모든 열을 input으로 설정
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, GPIO.PUD_DOWN)
         
        # 위에서 눌린 것으로 판단된 행을 output으로 설정 
        GPIO.setup(self.ROW[rowNum], GPIO.OUT)
        GPIO.output(self.ROW[rowNum], GPIO.HIGH)
 
        # 눌려진 열을 찾는 반복문, colNum은 0~3의 값만 가질 수 있음
        colNum = -1
        for j in range(len(self.COLUMN)):
            tmp = GPIO.input(self.COLUMN[j])
            if tmp == 1:
                colNum=j
                 
        # colNum이 0보다 작거나 3보다 큰 경우 눌린 것이 없다고 판단
        if colNum <0 or colNum >3:
            self.clear()
            return None
 
        # 입력받은 rowNum과 colNum에 해당하는 키패드의 숫자 반환
        self.clear()
        return self.KEYPAD[rowNum][colNum]
         
    def clear(self):
        # 모든 행과 열의 값을 초기화 해주는 메소드
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, GPIO.PUD_UP) 
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.IN, GPIO.PUD_UP)
        for i in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[i], GPIO.OUT)
            


                
if __name__ == '__main__':
    kp = Keypad()

#     while(True):
#         digit = None
#         while digit == None:
#             digit = kp.getKey()
#         print(digit)
#         time.sleep(0.5)

    seq = []
    for i in range(4):
        digit = None
        while digit == None:
            digit = kp.getKey()
            if (digit != None):
                print(digit)
        
        seq.append(digit)
        time.sleep(0.4)

    print(seq)

    if seq == [1,2,3,'#']:
        print('right')
    else:
        print('wrong')
