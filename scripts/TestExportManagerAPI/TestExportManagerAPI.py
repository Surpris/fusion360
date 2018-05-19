# -*- coding: utf-8 -*-

import adsk.core, adsk.fusion, traceback
import os.path, sys

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        
        # get active design
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
         
        # get all components in this design
        allComps = design.allComponents
         
        # get the script location
        scriptDir = os.path.dirname(os.path.realpath(__file__))        
         
        # create a single exportManager instance
        exportMgr = design.exportManager
        
        # export the component one by one with a specified format
        for comp in allComps:
            compName = comp.name
            fileName = scriptDir + "/" + compName
             
            # export the component with IGS format
            igesOptions = exportMgr.createIGESExportOptions(fileName, comp)
            exportMgr.execute(igesOptions)
             
            # export the component with SAT format
            satOptions = exportMgr.createSATExportOptions(fileName, comp)
            exportMgr.execute(satOptions)
         
            # export the component with SMT format
            smtOptions = exportMgr.createSMTExportOptions(fileName, comp)
            exportMgr.execute(smtOptions)
             
            # export the component with STP format
            stpOptions = exportMgr.createSTEPExportOptions(fileName, comp)
            exportMgr.execute(stpOptions)
             
            # export the component with F3D format
            archOptions = exportMgr.createFusionArchiveExportOptions(fileName, comp)
            exportMgr.execute(archOptions)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))