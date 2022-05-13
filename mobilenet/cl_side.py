import paho.mqtt.client as mqtt
server = "ip"
path = "test"

def on_connect(client, userdata, flags, rc):
    print("Connected "+str(rc))
    client.subscribe(path)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(server, 1883, 60)
client.loop_forever()

