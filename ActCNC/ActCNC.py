# Author-Ashwin Ramachandran, Pavel Koprov
# Description-Actuates the CNC Axes bassed on real time updates from the machine transfered over MQTT

#Reference: https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-6C0D8659-3294-4F3B-B2FC-ED120BAC2E27


import adsk.core, adsk.fusion, adsk.cam, traceback

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

        # move components in joints incrementally
        Xslider.slideValue = -20
        Yslider.slideValue = -10
        Zslider.slideValue = -15


        # # origins of coordinates
        # (Xorigin, _, _, _) = Xaxis.transform.getAsCoordinateSystem()
        # (Yorigin, _, _, _) = Yaxis.transform.getAsCoordinateSystem()
        # (Zorigin, _, _, _) = Zaxis.transform.getAsCoordinateSystem()


        # ui.messageBox(str(Xorigin.asArray()), "X Axis Table origin")
        # ui.messageBox(str(Yorigin.asArray()), "Y Axis Saddle origin")
        # ui.messageBox(str(Zorigin.asArray()), "Z Axis Ram origin")   



        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
