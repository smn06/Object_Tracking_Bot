import time
from time import sleep
from threading import Thread
import paho.mqtt.cli as mqtt
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

server = ""
path = ""
d = ""
xc = [0,0,0]
avx = 0.0
avy = 0.0
yc = [1,2,3]
farray = [0,0,0]
avface =0
fg = [0,0,0]
fm = ""

name = ""
xpos = 0
ypos = 0
fsize = 0;
amove = 400
movex = [1,2,3]
direct = "__n__"
act = 0
start_fd = 0
start_fn = 0
current = "face"
inittime = time.time()
dstring = ''
dist = 0.0
nts = 0
frun = True


servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)

wt = 0

def conn(cli, userd, flags, rc):
    print("Connected with result code "+str(rc))
    cli.subscribe(path)
    cli.subscribe("voice")
def msgg(cli, userd, msg):
    global d, xc, avx, yc, avy, name, xpos, ypos, act, fsize, avface, farray, amove, fg,  movex,direct, start_fd, fm, current, start_fn, inittime,  dist, dstring, wt, frun, nts
    tf_in = (str(msg.payload))
    if (tf_in.find('robot') != -1):
        wt = time.time() +10

    if (tf_in.find('coco') != -1):
        if (tf_in.find("dist") != -1):
            length = len(tf_in)
            pos1 = tf_in.find(':')  
            dstring = tf_in[(pos1+1):(length)]  
            dist = int(dstring)

    if (tf_in.find('face') != -1) and (time.time()<wt):
        GPIO.output(20, GPIO.HIGH)
        GPIO.output(21, GPIO.LOW)
        current = "face"
        act = not act
        print("follow")
        if (avface > 100):
            start_fd = avface
        else:
            start_fn = True
        farray[0] = 0
        farray[1] = 0
        farray[2] = 0
        avface = 0
        yc[0] = 0
        yc[1] = 0
        yc[2] = 0
        avy = 0
        xc[0] = 0
        xc[1] = 0
        xc[2] = 0
        avx = 0
        direct = "__n__"
        frun = 0 
        nts = True
    if((tf_in.find('person') !=-1) and (current == "face")):
        inittime = time.time()
        length = len(tf_in)
        pos1 = tf_in.find(':') 
        pos2 = tf_in.find(';')
        pos3 = tf_in.find('@')
        pos3 = tf_in.find('#')
        width = tf_in[(pos1+1):pos2]  
        width = int(width)
        height = tf_in[(pos2 + 1):pos3]  
        height = int(height)
        fsize = width * height
        farray[2] = farray[1]
        farray[1] = farray[0]
        farray[0] = fsize
        avface = farray[2] + farray[1] + farray[0]
        avface = avface / 3.0
        


        xpos = float(tf_in[(pos3 + 1):pos4])
        ypos = float(tf_in[(pos4+1):length])
        yc[2] = yc[1]
        yc[1] = yc[0]
        yc[0] = ypos
        avy = yc[2] + yc[1] + yc[0]
        avy = avy / 3.0
        xc[2] = xc[1]
        xc[1] = xc[0]
        xc[0] = xpos
        avx = xc[2] + xc[1] + xc[0]
        avx = avx / 3.0
        
        if start_fn == True:
            start_fd = fsize
            start_fn = 0


    if avx == 0:
        direct == "__n__"
    elif avx>470:
        direct = "left"
    elif avx<170:
        direct = "right"
    elif avx <470 and avx >170:
        direct = "neither"
    if (current == "face"):
        if (avface > (start_fd + 8000)):
            fm = "further"
        elif (avface < (start_fd -8000)):
            fm = "closer"
        else:
            fm = ""
    t = 0


        
cli = mqtt.Client()
cli.conn = conn
cli.connect(server, 1000, 50)

def exter():

    cli.msgg = msgg
    cli.loop_forever()




if __name__ == "__main__":
    t2 = Thread(target = exter)
    t2.setDaemon(True)
    t2.start()

