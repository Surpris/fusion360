# -*- coding: utf-8 -*-

"""ExportItems.py
Export specifiied items (under construction)
"""

import os
import time
import adsk.core, adsk.fusion, adsk.cam, traceback

exportOptions = ["F3D", "IGS", "SAT", "SMT", "STP"]

def getFullPath(file_or_fldr):
    if isinstance(file_or_fldr, adsk.core.DataFolder):
        if file_or_fldr.isRoot:
            return file_or_fldr.parentProject.name + "/" + "root"
        else:
            return getFullPath(file_or_fldr.parentFolder) + "/" + file_or_fldr.name
    else:
        return getFullPath(file_or_fldr.parentFolder) + "/" + file_or_fldr.name + "." + file_or_fldr.fileExtension
        
def walk(dataFolder):
    folders = dataFolder.dataFolders
    files = dataFolder.dataFiles
    result = []
    for file in files:
        result.append(file)
    for folder in folders:
        result.extend(walk(folder))
    return result

def exportActiveProduct(app, outputfldr, options=None, complete=False, is_overwrite=False):
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    exportMgr = design.exportManager
    if not complete:
        allComps = [design.rootComponent]
    else:
        allComps = design.allComponents
    if options is None:
        options = ["F3D"]
    elif isinstance(options, str):
        options = [options.upper()]
    elif isinstance(options, list):
        options = [option.upper() for option in options]
    try:
        for comp in allComps:
            compName = comp.name
            fileName = os.path.join(outputfldr, compName)
            for option in options:
                if option not in exportOptions:
                    print("{} is not supported.".format(option))
                    continue
                if option == "F3D":
                    export_option = exportMgr.createFusionArchiveExportOptions(fileName, comp)
                elif option == "IGS":
                    export_option = exportMgr.createIGESExportOptions(fileName, comp)
                elif option == "SAT":
                    export_option = exportMgr.createSATExportOptions(fileName, comp)
                elif option == "SMT":
                    export_option = exportMgr.createSMTExportOptions(fileName, comp)
                elif option == "STP":
                    export_option = exportMgr.createSTEPExportOptions(fileName, comp)
                if is_overwrite == False and os.path.exists(fileName + "." + option.lower()):
                    print("{} already exists.".format(fileName + "." + option.lower()))
                    continue
                exportMgr.execute(export_option)
            break
        return True
    except Exception as ex:
        print(ex)
        return False


def run(context):
    st = time.time()
    ui = None
    try:
        app = adsk.core.Application.get()
        docs = app.documents
        ui = app.userInterface
        hub = app.data.activeHub
        for ii, project in enumerate(hub.dataProjects):
            folder = project.rootFolder
            files = walk(folder)
            for file in files:
                if file.fileExtension == "f3d":
                    fldrpath = os.path.join(*getFullPath(file).split("/")[:-1])
                    outputfldr = os.path.join(os.environ.get('USERPROFILE'), "Downloads", fldrpath)
                    if not os.path.exists(outputfldr):
                        os.makedirs(outputfldr)
                    print("file:", file.name)
                    doc = docs.open(file) # "visible = False" will be supported in the future
                    
                    res = exportActiveProduct(app, outputfldr, options=["f3d", "stp"])
                    if not res:
                        print("{} cannot be exported.".format(file.name))
                    res = doc.close(False)
                    if not res:
                        raise Exception
#            break
    
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

    print("Elapsed time: {0:.2f}".format(time.time() - st))