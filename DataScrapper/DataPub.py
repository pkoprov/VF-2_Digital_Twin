import paho.mqtt.client as mqtt
import time
import pandas as pd
import random
import json

mqttBroker = 'broker.hivemq.com'
client1 = mqtt.Client('ashwin')
topic = 'FWH/CNC/Machine_coordinates'

while True:
    X = random.randint(-75, 0)
    Y = random.randint(-40, 0)
    Z = random.randint(0, 60)
    coordinates = {'X': X,
                   'Y': Y,
                   'Z': Z}
    message = json.dumps(coordinates)
    client1.connect(mqttBroker)
    client1.loop_start()
    try:
        client1.publish(topic, message, qos=1)
        print(f"Publishing {coordinates} to {topic}")
    except:
        print('Something went wrong')
    time.sleep(0.7)
