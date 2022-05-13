import paho.mqtt.client as mqtt
import os
import cv2
import sys
import numpy
import ntpath
import argparse
import time
from threading import Thread


import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

import edgetpu.detection.engine
from edgetpu.utils import image_processing

from imutils.video import FPS
from imutils.video import VideoStream

server = " "
path = " "

msg = " "
act = False
h = 0
arg = None

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("voice")

client = mqtt.Client()
client.on_connect = on_connect
client.connect(server, 1883, 60)



def runB():
    client.mssg = mssg
    client.loop_forever()

def mssg(client, userdata, msg):
    global msg, act, h
    msg = (str(msg.payload))
    if msg.find('robot') != -1:
        h = time.time() +10
    elif (msg.find('face') != -1) or (msg.find('coco') != -1):
        act = True


def read(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        ret = {}
    for line in lines:
        pair = line.strip().split(maxsplit=1)
        ret[int(pair[0])] = pair[1].strip()
    return ret

def main2():

    labels = read(arg.labels) if arg.labels else None

    font = PIL.ImageFont.truetype("*.ttf", 15)

    if arg.picamera:
        print("internal camera.")
    else:
        print("external camera")


    engine = edgetpu.detection.engine.DetectionEngine('mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite')

    vids = VideoStream(usePiCamera=arg.picamera, resolution=(640, 480)).start()
    time.sleep(1)

    fps = FPS().start()

    while msg.find('coco') != -1:
        try:

            screenshot = vids.read()

            image = PIL.Image.fromarray(screenshot)

            start = time.time()
            inferenceResults = engine.DetectWithImage(image, threshold=arg.confidence, keep_aspect_ratio=True, relative_coord=False, top_k=arg.maxobjects)
            elapsedMs = time.time() - start

            if( cv2.waitKey( 2 ) & 0xFF == ord( 'q' ) ):
                fps.stop()
                break

            fps.update()

        except KeyboardInterrupt:
            fps.stop()
            break


    cv2.destroyAllWindows()
    vids.stop()
    time.sleep(2)

def main():

    labels = read(arg.labels) if arg.labels else None

    font = PIL.ImageFont.truetype("*.ttf", 15)

    if arg.picamera:
        print("internal camera.")
    else:
        print("external camera")


    engine = edgetpu.detection.engine.DetectionEngine('mobilenet_ssd_v2_face_quant_postprocess_edgetpu.tflite')#'mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite')

    vids = VideoStream(usePiCamera=arg.picamera, resolution=(640, 480)).start()
    time.sleep(1)

    fps = FPS().start()

    while msg.find('face') != -1:
        try:

            screenshot = vids.read()
            image = PIL.Image.fromarray(screenshot)

            start = time.time()
            inferenceResults = engine.DetectWithImage(image, threshold=arg.confidence, keep_aspect_ratio=True, relative_coord=False, top_k=arg.maxobjects)
            elapsedMs = time.time() - start

            if( cv2.waitKey( 2 ) & 0xFF == ord( 'q' ) ):
                fps.stop()
                break

            fps.update()

        except KeyboardInterrupt:
            fps.stop()
            break



    cv2.destroyAllWindows()
    vids.stop()
    time.sleep(2)

