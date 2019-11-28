# 얼굴 인식 도어락
- Facial recognition Door Lock with Raspberry Pi using Python3

## Target System
- Linux raspberrypi 4.19.75-v7+ #1270 SMP Tue Sep 24 18:45:11 BST 2019 armv7l GNU/Linux
- cv2.__version__ = '4.1.1'
- Python 3.7.3 (default, Apr  3 2019, 05:39:12) 
[GCC 8.2.0] on linux

## 사용한 부품
- Tactile Switch

![tswitch](https://order.pay.naver.com/proxy/phinf/shop1/20170826_174/koroma_1503726703375yskJt_JPEG/27033004002463862_1987610978.jpg?type=m80)
- Limit Switch

![lswitch](https://order.pay.naver.com/proxy/phinf/shop1/20191017_170/1571321492776FBO3H_JPEG/8682231410284309_843330882.jpg?type=m80)
- Max7219 with 8x8 Dot Matrix

![matrix](https://order.pay.naver.com/proxy/phinf/shop1/20170531_117/koroma_1496193585169u4ikh_JPEG/19500764811954828_354388114.jpg?type=m80)
- Membrane Keypad

![keypad](https://shop-phinf.pstatic.net/20170921_257/koroma_1505959223963Shqn6_JPEG/29266417503682591_39724661.jpg?type=m120)
- Pi Camera

![camera](https://order.pay.naver.com/proxy/phinf/shop1/20171116_258/koroma_1510797329629YLH53_JPEG/34104489251011958_-1087853166.JPG?type=m80)

## 사용한 파이썬 모듈
- time
- RPi.GPIO
- os
- numpy
- cv2
- pickle
- sys
- picamera.array.PiRGBArray
- picamera.PiCamera
- PIL.Image
- spidev
- pad4pi

## 설치한 라이브러리
- libhdf5-dev
- libatlas-base-dev
- libjasper-dev 
- libqtgui4 
- libqt4-test
- build-essential 
- cmake
- libjpeg-dev 
- libtiff5-dev 
- libpng12-dev
- libavcodec-dev 
- libavformat-dev 
- libswscale-dev 
- libxvidcore-dev 
- libx264-dev 
- libxine2-dev
- libv4l-dev 
- v4l-utils
- libgstreamer1.0-dev 
- libgstreamer-plugins-base1.0-dev
- libgtk2.0-dev
- mesa-utils 
- libgl1-mesa-dri 
- libgtkgl2.0-dev 
- libgtkglext1-dev
- gfortran 
- libeigen3-dev
- python2.7-dev
- python3-dev

## Reference

- 얼굴인식 관련 코드

https://maker.pro/raspberry-pi/projects/how-to-create-a-facial-recognition-door-lock-with-raspberry-pi

- 4x4 멤브레인 키패드

https://www.youtube.com/watch?v=yYnX5QodqQ4

- max7219와 spidev

https://pypi.org/project/spidev/

https://datasheets.maximintegrated.com/en/ds/MAX7219-MAX7221.pdf

- openCV 설치

https://webnautes.tistory.com/916

- GPIO 제어

https://pythonhosted.org/RPIO/

https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/


