# -*- coding: utf-8 -*-

"""ListUpFiles.py
List up all the files
"""

import os
import time
import adsk.core, adsk.fusion, adsk.cam, traceback

exportOptions = ["F3D", "IGS", "SAT", "SMT", "STP", "STEP"]

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

def run(context):
    st = time.time()
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        hub = app.data.activeHub
        summary = ""
        for ii, project in enumerate(hub.dataProjects):
            folder = project.rootFolder
            files = walk(folder)
            full_paths = []
            for file in files:
                full_paths.append(getFullPath(file))
            summary += "\n".join(full_paths) + "\n"
#            if ii == 0:
#                break
        
        outputPath = os.path.join(os.environ.get('USERPROFILE'), "Downloads", "list.txt")
        with open(outputPath, "w") as ff:
            ff.write(summary)
    
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

    print("Elapsed time: {0:.2f}".format(time.time() - st))