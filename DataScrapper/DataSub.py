import paho.mqtt.client as mqtt
import time
import pandas as pd
import json

mqttBroker = 'broker.hivemq.com'
mqtt_client = mqtt.Client('kms')
topic = 'FWH/CNC/Machine_coordinates'


def on_message(client, userdata, msg):
    x = msg.payload
    update_sliders(x)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        mqtt_client.subscribe(topic + '/#')
    else:
        print(f"Failed to connect, return code {rc}", "Error\t")


def update_sliders(x):
    coordinates = json.loads(x)
    print(coordinates)
    x = coordinates['X']
    y = coordinates['Y']
    z = coordinates['Z']
    print(f' X= {x}, Y={y}, Z= {z}')


mqtt_client.connect(mqttBroker)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.loop_forever()
