from time import sleep
from Bluetin_Echo import echo_val
import paho.mqtt.publish as publish

server = ""
path = ""
tp = 20
ep = 8
echo_val = [echo_val(tp, ep)]
def main():
    sleep(0.1)
    for c in range(1, 2):
        for f in range(0, len(echo_val)):
            result = echo_val[f].read('cm', 3)
            print (result)
            result2 = int (result)
            if result2 > 0:
                publish.single(path, 'coco distance:' + str (result2), hostname=server)

if __name__ == '__main__':
    while True:
        main()

