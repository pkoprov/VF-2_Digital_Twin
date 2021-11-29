import paho.mqtt.client as mqtt
import time
import pandas as pd
import random
import json
import config
import psycopg2 as pg
import numpy as np

mqttBroker = 'broker.hivemq.com'
client1 = mqtt.Client('Hass')
topic = 'FWH/CNC/Machine_coordinates'

# Connect to DataBase
conn = pg.connect(f"host = {config.host} port = {config.port} dbname={config.db} user={config.user} "
                  f"password={config.password}")

while True:
    CMD = f'select * from "VF-2_1" where "Power-on Time (total)" IS NOT NULL order by "Year, month, day" desc, "Power-on Time (total)" desc limit 1'
    df = pd.read_sql_query(CMD, conn)
    df.replace([None], np.nan, inplace=True)
    X = float(df['Present machine coordinate position X'][0])
    Y = float(df['Present machine coordinate position Y'][0])
    Z = float(df['Present machine coordinate position Z'][0])
    coordinates = {'X': X,
                   'Y': Y,
                   'Z': Z}
    message = json.dumps(coordinates)
    client1.connect(mqttBroker)
    client1.loop_start()
    try:
        client1.publish(topic, message, qos=1, retain=True)
        print(f"Publishing {coordinates} to {topic}")
    except:
        print('Something went wrong')
    time.sleep(0.7)
