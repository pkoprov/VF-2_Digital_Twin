# Author-Ashwin Ramachandran, Pavel Koprov
# Description-Actuates the CNC Axes bassed on real time updates from the machine transfered over MQTT
#Reference: https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-6C0D8659-3294-4F3B-B2FC-ED120BAC2E27

from adsk import doEvents, terminate
import adsk.core, adsk.fusion, adsk.cam, traceback
import json
import time

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        try: 
            from .Modules.paho.mqtt import client as mqtt
        except:
            ui.messageBox("Error")
        
        mqttBroker = 'broker.hivemq.com'
        mqtt_client = mqtt.Client('MyCNC')
        topic = 'FWH/CNC/Machine_coordinates'
        
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


        def on_message(client, userdata, msg):
            x = msg.payload
            update_sliders(x)


        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                ui.messageBox("Connected to MQTT Broker!", "Connected!")
            else:
                ui.messageBox(f"Failed to connect, return code {rc}", "Error\t")

        def update_sliders(x):
            coordinates = json.loads(x)
            Xslider.slideValue = coordinates['X']
            Yslider.slideValue = coordinates['Y']
            Zslider.slideValue = coordinates['Z']
            adsk.doEvents()
            app.activeViewport.refresh()
                
           
        try:
            mqtt_client.connect(mqttBroker)
            mqtt_client.on_connect = on_connect
            mqtt_client.on_message = on_message
            mqtt_client.subscribe(topic + '/#')
            mqtt_client.loop_forever()
        except KeyboardInterrupt:
            ui.messageBox("User ended script", "Goodbye")        
        
            
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
