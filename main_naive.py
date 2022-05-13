import cv2
import numpy as np
from _thread import *
import time
import RPi.GPIO as GPIO
import imutils
from imutils.video import WebcamVideoStream
GPIO.setmode(GPIO.BCM)

lf=11
lb=10
rf=8
rb=9

GPIO.setup(lf, GPIO.OUT)
GPIO.setup(lb, GPIO.OUT)
GPIO.setup(rf, GPIO.OUT)
GPIO.setup(rb, GPIO.OUT)


def stopMotor():
    GPIO.output(lb,0)
    GPIO.output(rb,0)
    GPIO.output(lf,0)
    GPIO.output(rf,0)


def right():
    GPIO.output(lf,1)
    GPIO.output(lb,0)
    GPIO.output(rf,0)
    GPIO.output(rb,1)


def left():
    GPIO.output(lf,0)
    GPIO.output(lb,1)
    GPIO.output(rf,1)
    GPIO.output(rb,0)


def forward():
    GPIO.output(lf,1)
    GPIO.output(rf,1)


def backward():
    GPIO.output(lb,1)
    GPIO.output(rb,1)


def drive():
    global mina,maxa,t,s,xx,wid,w,h
    while not tstop:
        if t==1 and s:
            if (xx > 3*wid/4):
                right()
                time.sleep(0.015)
            elif (xx < wid/4):
                left()
                time.sleep(0.015)
            elif (w*h > maxa):
                backward()
                time.sleep(0.025)
            elif (w*h < mina):
                forward()
                time.sleep(0.025)
            
            stopMotor()
            time.sleep(0.0125)

        else:
            stopMotor()
    GPIO.cleanup()
            


if __name__ == "__main__":

    global xx,w,h,t,mina,maxa,s,wid,tstop
    tstop = 0
    s = 0 
    t = 0
    lthresh = np.array([15, 50, 50])
    hthresh = np.array([225, 250, 255])
    cam = WebcamVideoStream(src=0).start()

    flag = 1
    start_new_thread(drive,())
    while 1:
        frame = cam.read() 
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lthresh, hthresh)
        mask = cv2.erode(mask, None, iterations=4)
        mask = cv2.dilate(mask, None, iterations=4) 
        contour = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        contour = imutils.grab_contours(contour)

        heit,wid,_ = frame.shape
        cv2.rectangle(frame,(int(wid/4),0),(int(3*wid/4),heit),(150,150,255),2)

        if len(contour)>0:
            t = 1
            c = maxa(contour, key=cv2.contourArea)
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(150,150,255),2)
            moment = cv2.moments(c)
            xx = int(moment['moment10']/moment['moment00'])
            yy = int(moment['moment01']/moment['moment00'])

            if flag:
                maxa = 3*w*h/2
                mina = w*h/2

        else:
            t = 0

        cv2.imshow("Frame",frame)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            tstop = 1
            break
        elif k == ord('l') and t==1:
            flag = 0
            s = 1
cam.stop()
cv2.destroyAllWindows()
