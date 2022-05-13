import cv2
import numpy as np

cam = cv2.VideoCapture(0)

cv2.namedWindow('window')
a,b,c,d,e,f= 100,150,255,120,170,255
cv2.createTrackbar('c_h','window',0,a)
cv2.createTrackbar('c_s','window',0,b)
cv2.createTrackbar('c_v','window',0,c)

cv2.createTrackbar('r_h','window',0,d)
cv2.createTrackbar('r_s','window',0,e)
cv2.createTrackbar('r_v','window',0,f)

while(True):

    ret, frame = cam.read()
    frame = cv2.flip(frame,1)
    nframe = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    c_h = cv2.getTrackbarPos('c_h','window')
    c_s = cv2.getTrackbarPos('c_s','window')
    c_v = cv2.getTrackbarPos('c_v','window')
    r_h = cv2.getTrackbarPos('r_h','window')
    r_s = cv2.getTrackbarPos('r_s','window')
    r_v = cv2.getTrackbarPos('r_v','window')
    low = np.array([c_h,c_s,c_v])
    high = np.array([r_h,r_s,r_v])
    mask = cv2.inRange(nframe,low,high)
    output = cv2.bitwise_and(frame,frame,mask=mask)
    cv2.imshow('window',frame)
    cv2.imshow('output',output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()