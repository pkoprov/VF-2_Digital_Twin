import paho.mqtt.client as mqtt
import time
import pandas as pd
import random
import json

mqttBroker = 'broker.hivemq.com'
client1 = mqtt.Client('ashwin')
topic = 'FWH/CNC/Machine_coordinates'

data = pd.read_csv('Coordinates.csv')
x = data['x'].tolist()
y = data['y'].tolist()
z = data['z'].tolist()
for i in range(len(x)):
    X = x[i]
    Y = y[i]
    Z = z[i]
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
    time.sleep(0.5)
