import json

import paho.mqtt.client as mqtt
import random


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("sensor/#", 2)


def on_subscribe(client, userdata, mid, granted_qos):
    print('subscribed')


def on_publish(client, userdata, result):
    print("data published \n")
    pass


def on_message(client, userdata, msg):
    from .service import DeviceDataQueries

    payload = str(msg.payload.decode('utf8'))
    dict_payload = json.loads(payload)
    DeviceDataQueries.create_one(data=dict_payload)


client_id = f'python-mqtt-{random.randint(0, 1000)}'
client = mqtt.Client(client_id)
client.connect("192.168.43.109", 1883, 60)
client.username_pw_set(username="admin", password="public")
client.on_publish = on_publish
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message
