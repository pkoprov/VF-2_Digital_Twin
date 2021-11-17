import paho.mqtt.client as mqtt
import time
import pandas as pd

mqttBroker = 'broker.hivemq.com'
mqtt_client = mqtt.Client('kms')
topic = 'FWH/CNC/Machine_coordinates'
XTopic = topic + '/X'
YTopic = topic + '/Y'
ZTopic = topic + '/Z'

topics = [XTopic, YTopic, ZTopic]


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    print(f'Message! {message} on topic {msg.topic}')


mqtt_client.connect(mqttBroker)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.subscribe("FWH/CNC/Machine_coordinates/#")
mqtt_client.loop_forever()
