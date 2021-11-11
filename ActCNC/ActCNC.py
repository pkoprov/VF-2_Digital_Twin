# Author-Ashwin Ramachandran
# Description-Actuates the CNC Axes bassed on real time updates from the machine transfered over MQTT

#Reference: https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-6C0D8659-3294-4F3B-B2FC-ED120BAC2E27

import adsk.core, adsk.fusion, adsk.cam, traceback
from coordinates import get_coords

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # Create a document.
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)

        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)

        # Get the root component of the active design
        rootComp = design.rootComponent




    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
