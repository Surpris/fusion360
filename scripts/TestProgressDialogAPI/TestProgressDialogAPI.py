#Author-
#Description-

import adsk.core, adsk.fusion, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        # Create a document.
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)        
        
        # Set styles of progress dialog.
        progressDialog = ui.createProgressDialog()
        progressDialog.cancelButtonText = 'Cancel'
        progressDialog.isBackgroundTranslucent = False
        progressDialog.isCancelButtonShown = True
        
        # Show dialog
        progressDialog.show('Progress Dialog', 'Percentage: %p, Current Value: %v, Total steps: %m', 0, 50, 1)
        
        # Draw sketches and update status.
        design = app.activeProduct
        rootComp = design.rootComponent
        sketches = rootComp.sketches
        sketch = sketches.add(rootComp.xZConstructionPlane)
        sketchCircles = sketch.sketchCurves.sketchCircles
        centerPt = adsk.core.Point3D.create(0, 0, 0)
        for i in range(50):
            # If progress dialog is cancelled, stop drawing.
            if progressDialog.wasCancelled:
                break
            sketchCircles.addByCenterRadius(centerPt, i+1)
            # Update progress value of progress dialog
            progressDialog.progressValue = i+1
        
        # Hide the progress dialog at the end.
        progressDialog.hide()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))