# Author-Ashwin Ramachandran, Pavel Koprov
# Description-Actuates the CNC Axes bassed on real time updates from the machine transfered over MQTT
#Reference: https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-6C0D8659-3294-4F3B-B2FC-ED120BAC2E27

import adsk.core, adsk.fusion, adsk.cam, traceback
import Values

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
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
            X = Values.X
            Y = Values.Y
            Z = Values.Z   
        except:
            ui.messageBox("Something is Wrong", "Error\t") 

        # move components in joints incrementally
        for i in range(0, len(X)-1):
            Xslider.slideValue = X[i]
            Yslider.slideValue = Y[i]
            Zslider.slideValue = Z[i]
            ui.messageBox(f'{X[i]},{Y[i]},{Z[i]}', 'New Coordinates')
   

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
