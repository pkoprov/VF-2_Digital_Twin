# Author-Ashwin Ramachandran, Pavel Koprov
# Description-Actuates the CNC Axes based on real time updates from the machine transferred over MQTT
#Reference: https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-6C0D8659-3294-4F3B-B2FC-ED120BAC2E27

from adsk import doEvents, terminate
import adsk.core, adsk.fusion, adsk.cam, traceback
import json
import time
# import paho.mqtt.client as mqtt


carry_on = True

def run(context):

    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        try: 
            from .Modules.paho.mqtt import client as mqtt
        except:
            ui.messageBox("Error")


        def on_message(client, userdata, msg):
            # print(msg.payload)
            global carry_on
            if msg.topic == "DT":
                if msg.payload.decode().lower() == "stop":
                    carry_on = False
            else:
                msg = json.loads(msg.payload)
                data = "Present machine coordinate position "
                coord_list = "XYZ"
                coord_keys = [data + coord for coord in coord_list]
                coord_val = [float(value) for key, value in msg.items() if key in coord_keys]
                update_sliders(coord_val)

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                # print("Connected!", "MQTT Status")
                ui.messageBox("Connected!", "MQTT Status")
            else:
                # print(f"Error\t\nFailed to connect, return code {rc}", "MQTT Status")
                ui.messageBox(f"Error\t\nFailed to connect, return code {rc}", "MQTT Status")

        def update_sliders(coordinates):
            Xslider.slideValue = coordinates[0]*2.54
            Yslider.slideValue = coordinates[1]*2.54
            Zslider.slideValue = (coordinates[2]- 4.1481)*2.54-2.824
            doEvents()
            app.activeViewport.refresh()


        mqttBroker = '192.168.10.4'
        mqtt_client = mqtt.Client('MyCNC')
        topic = 'spBv1.0/FWH2200/DDATA/VF-2_2_RPI/VF-2_2'
        cmd = "DT"
        
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        if not design:
            ui.messageBox('No active Fusion design', 'No Design')
            return

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Define the occurances of X axis table, Y axis saddle and Z axis ramp coordinates
        Xaxis = "X Axis Table:1"
        Xaxis = rootComp.occurrences.itemByName(Xaxis)
        Yaxis = "Y Axis Saddle:1"
        Yaxis = rootComp.occurrences.itemByName(Yaxis)
        Zaxis = "Z Axis Ram2:1"
        Zaxis = rootComp.occurrences.itemByName(Zaxis)

        # define slider joints for corresponding components
        Xslider = adsk.fusion.SliderJointMotion.cast(Xaxis.asBuiltJoints.itemByName("Xslider").jointMotion)
        Yslider = adsk.fusion.SliderJointMotion.cast(Yaxis.asBuiltJoints.itemByName("Yslider").jointMotion)
        Zslider = adsk.fusion.SliderJointMotion.cast(Zaxis.asBuiltJoints.itemByName("Zslider").jointMotion)

        try:
            mqtt_client.connect(mqttBroker)
            mqtt_client.on_connect = on_connect
            mqtt_client.on_message = on_message
            mqtt_client.subscribe(topic)
            mqtt_client.subscribe(cmd)
            mqtt_client.loop()
        except:
            ui.messageBox("Disconnected!", "MQTT Status")


        try:
            while carry_on:
                mqtt_client.loop()
                time.sleep(0.1)
        except:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            pass
        finally:
            # print("Disconnected!", "MQTT Status")
            ui.messageBox("Disconnected!", "MQTT Status")
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
