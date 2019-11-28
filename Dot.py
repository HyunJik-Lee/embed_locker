import spidev
import time

class Dot:
    def __init__(self):
        #딜레이와 레지스터에 대해서 define
        self.delay = 0.3
        self.NO_OP        = 0x0
        self.DIGIT_0      = 0x1
        self.DIGIT_1      = 0x2
        self.DIGIT_2      = 0x3
        self.DIGIT_3      = 0x4
        self.DIGIT_4      = 0x5
        self.DIGIT_5      = 0x6
        self.DIGIT_6      = 0x7
        self.DIGIT_7      = 0x8
        self.DECODE_MODE  = 0x9
        self.INTENSITY    = 0xA
        self.SCAN_LIMIT   = 0xB
        self.SHUTDOWN     = 0xC
        self.DISPLAY_TEST = 0xF
        
        #각각의 모양을 만들기 위해서 전달해야하는 값들을 list로 표현
        self.oshape1 = [0x00, 0x00, 0x00, 0x18, 0x18, 0x00, 0x00, 0x00]
        self.oshape2 = [0x00, 0x00, 0x18, 0x24, 0x24, 0x18, 0x00, 0x00]
        self.oshape3 = [0x00, 0x18, 0x24, 0x42, 0x42, 0x24, 0x18, 0x00]
        self.oshape4 = [0x3C, 0x66, 0xC3, 0x81, 0x81, 0xC3, 0x66, 0x3C]
        self.xshape1 = [0x00, 0x00, 0x00, 0x18, 0x18, 0x00, 0x00, 0x00]
        self.xshape2 = [0x00, 0x00, 0x24, 0x18, 0x18, 0x24, 0x00, 0x00]
        self.xshape3 = [0x00, 0x66, 0x7E, 0x3C, 0x3C, 0x7E, 0x66, 0x00]
        self.xshape4 = [0xC3, 0xE7, 0x7E, 0x3C, 0x3C, 0x7E, 0xE7, 0xC3]
        self.lshape1 = [0xF9, 0x89, 0x8E, 0x88, 0x88, 0x88, 0x88, 0xF8]
        self.lshape2 = [0xF8, 0x88, 0x8E, 0x89, 0x88, 0x88, 0x88, 0xF8]
        self.lshape3 = [0xF8, 0x88, 0x8E, 0x89, 0x89, 0x88, 0x88, 0xF8]
        self.lshape4 = [0xF8, 0x88, 0x8E, 0x89, 0x89, 0x8E, 0x88, 0xF8]
        self.qshape1 = [0x04, 0x06, 0x07, 0x03, 0x01, 0x00, 0x00, 0x00]
        self.qshape2 = [0x04, 0x06, 0x07, 0x03, 0x03, 0x03, 0x02, 0x00]
        self.qshape3 = [0x04, 0x06, 0x07, 0x13, 0x13, 0x1F, 0x0E, 0x04]
        self.qshape4 = [0x04, 0x06, 0x07, 0xB3, 0xB3, 0x1F, 0x0E, 0x04]
        self.sshape1 = [0x3C, 0x42, 0x81, 0x81, 0x81, 0x81, 0x42, 0x3C]
        self.sshape2 = [0x3C, 0x42, 0x85, 0x81, 0x81, 0x85, 0x42, 0x3C]
        self.sshape3 = [0x3C, 0x42, 0x85, 0xA1, 0xA1, 0x85, 0x42, 0x3C]
        self.sshape4 = [0x3C, 0x52, 0xA5, 0xA1, 0xA1, 0xA5, 0x52, 0x3C]
        self.pshape1 = [0x03, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.pshape2 = [0x1B, 0x0B, 0x00, 0x03, 0x01, 0x00, 0x00, 0x00]
        self.pshape3 = [0xDB, 0x5B, 0x00, 0x1B, 0x0B, 0x00, 0x03, 0x01]
        self.pshape4 = [0xDB, 0xDB, 0x00, 0xDB, 0x5B, 0x00, 0x1B, 0x0B]
        self.pshape5 = [0xDB, 0xDB, 0x00, 0xDB, 0xDB, 0x00, 0xDB, 0xDB]
        
        
        #SPI통신을 위해서 초기화
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.max_speed_hz=1000000
        self.spi.no_cs=False
        self.spi.xfer2([self.SCAN_LIMIT, 7])
        self.spi.xfer2([self.DECODE_MODE, 0])
        self.spi.xfer2([self.DISPLAY_TEST, 0])
        self.spi.xfer2([self.INTENSITY, 4])
        self.spi.xfer2([self.SHUTDOWN, 1])

        for register in range(8):
            self.spi.xfer2([register+1, 0x00])
    
    #O모양을 표시하는 메소드
    def success(self):
        for idx in range(8):
            data = [idx+1, self.oshape1[idx]]
            self.spi.xfer2(data)
        time.sleep(self.delay)
        for idx in range(8):
            data = [idx+1, self.oshape2[idx]]
            self.spi.xfer2(data)
        time.sleep(self.delay)
        for idx in range(8):
            data = [idx+1, self.oshape3[idx]]
            self.spi.xfer2(data)
        time.sleep(self.delay)
        for idx in range(8):
            data = [idx+1, self.oshape4[idx]]
            self.spi.xfer2(data)
        time.sleep(self.delay)
        self.clear()
        return None
    
    #X모양을 표시하는 메소드
    def fail(self):
        for idx in range(8):
            data = [idx+1, self.xshape1[idx]]
            self.spi.xfer2(data)
        time.sleep(self.delay)
        for idx in range(8):
            data = [idx+1, self.xshape2[idx]]
            self.spi.xfer2(data)
        time.sleep(self.delay)
        for idx in range(8):
            data = [idx+1, self.xshape3[idx]]
            self.spi.xfer2(data)
        time.sleep(self.delay)
        for idx in range(8):
            data = [idx+1, self.xshape4[idx]]
            self.spi.xfer2(data)
        time.sleep(self.delay)
        self.clear()
        return None
    
    #잠그는 모양을 표시하는 메소드
    def lock(self):
        for idx in range(8):
            data = [idx+1, self.lshape1[idx]]
            self.spi.xfer2(data)
        time.sleep(self.delay)
        for idx in range(8):
            data = [idx+1, self.lshape2[idx]]
            self.spi.xfer2(data)
        time.sleep(self.delay)
        for idx in range(8):
            data = [idx+1, self.lshape3[idx]]
            self.spi.xfer2(data)
        time.sleep(self.delay)
        for idx in range(8):
            data = [idx+1, self.lshape4[idx]]
            self.spi.xfer2(data)
        time.sleep(self.delay)
        self.clear()
        return None
        
    #잠금해제하는 모양을 표시하는 메소드
    def unlock(self):
        for idx in range(8):
            data = [idx+1, self.lshape4[idx]]
            self.spi.xfer2(data)
        time.sleep(self.delay)
        for idx in range(8):
            data = [idx+1, self.lshape3[idx]]
            self.spi.xfer2(data)
        time.sleep(self.delay)
        for idx in range(8):
            data = [idx+1, self.lshape2[idx]]
            self.spi.xfer2(data)
        time.sleep(self.delay)
        for idx in range(8):
            data = [idx+1, self.lshape1[idx]]
            self.spi.xfer2(data)
        time.sleep(self.delay)
        self.clear()
        return None
    
    #얼굴 인식 물음표 표시 메소드
    def question(self):
        delay = self.delay * 1.5
        for idx in range(8):
            data = [idx+1, self.qshape1[idx]]
            self.spi.xfer2(data)
        time.sleep(delay)
        for idx in range(8):
            data = [idx+1, self.qshape2[idx]]
            self.spi.xfer2(data)
        time.sleep(delay)
        for idx in range(8):
            data = [idx+1, self.qshape3[idx]]
            self.spi.xfer2(data)
        time.sleep(delay)
        for idx in range(8):
            data = [idx+1, self.qshape4[idx]]
            self.spi.xfer2(data)
        time.sleep(delay)
        self.clear()
        return None

    #얼굴 인식 스마일 표시 메소드
    def smile(self):
        delay = self.delay * 1.2
        for idx in range(8):
            data = [idx+1, self.sshape1[idx]]
            self.spi.xfer2(data)
        time.sleep(delay)
        for idx in range(8):
            data = [idx+1, self.sshape2[idx]]
            self.spi.xfer2(data)
        time.sleep(delay)
        for idx in range(8):
            data = [idx+1, self.sshape3[idx]]
            self.spi.xfer2(data)
        time.sleep(delay)
        for idx in range(8):
            data = [idx+1, self.sshape4[idx]]
            self.spi.xfer2(data)
        time.sleep(delay)
        self.clear()
        return None

    #비밀번호 모드 표시 메소드
    def password(self):
        delay = self.delay
        for idx in range(8):
            data = [idx+1, self.pshape1[idx]]
            self.spi.xfer2(data)
        time.sleep(self.delay)
        for idx in range(8):
            data = [idx+1, self.pshape2[idx]]
            self.spi.xfer2(data)
        time.sleep(self.delay)
        for idx in range(8):
            data = [idx+1, self.pshape3[idx]]
            self.spi.xfer2(data)
        time.sleep(self.delay)
        for idx in range(8):
            data = [idx+1, self.pshape4[idx]]
            self.spi.xfer2(data)
        time.sleep(self.delay)
        for idx in range(8):
            data = [idx+1, self.pshape5[idx]]
            self.spi.xfer2(data)
        time.sleep(self.delay)
        self.clear()

    #출력 후 Dotmatrix를 초기화 하는 메소
    def clear(self):
        for register in range(8):
            self.spi.xfer2([register+1, 0x00])
        return None

        
if __name__ == '__main__':
    dot = Dot()
    
    dot.success()
    dot.fail()
    dot.lock()
    dot.unlock()
    dot.question()
    dot.smile()
    dot.password()
    dot.spi.close()
    
