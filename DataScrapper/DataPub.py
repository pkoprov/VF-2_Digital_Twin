import paho.mqtt.client as mqtt
import time
import pandas as pd
import random

mqttBroker = 'broker.hivemq.com'
client1 = mqtt.Client('ashwin')
topic = 'FWH/CNC/Machine_coordinates'
XTopic = topic + '/X'
YTopic = topic + '/Y'
ZTopic = topic + '/Z'

while True:
    X = random.randint(-75, 0)
    Y = random.randint(-40, 0)
    Z = random.randint(0, 60)
    client1.connect(mqttBroker)
    client1.loop_start()
    try:
        client1.publish(XTopic, X, qos=1)
        print(f'Publishing {X} to {XTopic}\n')
        client1.publish(YTopic, Y, qos=1)
        print(f'Publishing {Y} to {YTopic}\n')
        client1.publish(topic + '/Z', Z, qos=1)
        print(f'Publishing {Z} to {ZTopic}\n')
    except:
        print('Something went wrong')
    time.sleep(0.1)
