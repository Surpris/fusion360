# -*- coding: utf-8 -*-

"""TestDocumentOpenAPI.py
Test to open document via Fusion 360 API
"""

#import os
import time
import adsk.core, adsk.fusion, adsk.cam, traceback

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
        docs = app.documents
        ui = app.userInterface
        hub = app.data.activeHub
        for ii, project in enumerate(hub.dataProjects):
            folder = project.rootFolder
            files = walk(folder)
            for file in files:
                docs.open(file)
                break
            if ii == 0:
                break

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

    print("Elapsed time: {0:.2f}".format(time.time() - st))