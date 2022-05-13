import cv2
import argparse
import imutils
import time
import paho.mqtt.publish as pub
from edgetpu.detection.engine import DetectionEngine
from imutils.video import VideoStream
from PIL import Image
server = ""
path = ""
parser = argparse.ArgumentParser()
args = vars(parser.parse_args())
label = {}
for row in open(args["label"]):
    (classID, label) = row.strip().split(maxsplit=1)
    label[int(classID)] = label.strip()
model = DetectionEngine(args["model"])
video = VideoStream(src=0).start()

time.sleep(1.0)

while True:
    f = video.read()
    f = imutils.resize(f, width=500)
    o_f = f.copy()

    f = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
    f = Image.fromarray(f)
    start = time.time()
    output = model.DetectWithImage(f, threshold=args["con"])
    end = time.time()
    for r in output:
        bbox = r.bounding_box.flatten().astype("int")
        (xx, yy, endX, endY) = bbox
        label = label[r.label_id]
        pub.single(path, str(xx), hostname=server)

        cv2.rectangle(o_f, (xx, yy), (endX, endY), (150, 255, 150), 2)
        if (yy - 20 > 20):
            y = yy - 20
        else:   
            yy + 20
        text = "{}: {:.2f}%".format(label, r.score * 100)
        cv2.putText(o_f, text, (xx, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 255, 150), 2)

    cv2.imshow("f", o_f)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):

        cv2.destroyAllWindows()
        video.stop()


