# -*- coding: utf-8 -*-

#Author-
#Description-

import adsk.core, adsk.fusion, traceback
import os.path

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
            
        msg = ''
        # Set styles of file dialog.
        fileDlg = ui.createFileDialog()
        fileDlg.isMultiSelectEnabled = True
        fileDlg.title = 'Fusion File Dialog'
        fileDlg.filter = '*.*'
        
        # Show file open dialog
        dlgResult = fileDlg.showOpen()
        if dlgResult == adsk.core.DialogResults.DialogOK:
            msg += '\nopen files:'
            for filename in fileDlg.filenames:
                msg += '\n\t{}'.format(filename)       
        
        # Show file save dialog
        dlgResult = fileDlg.showSave()
        if dlgResult == adsk.core.DialogResults.DialogOK:
            msg += '\nsave to: {}'.format(fileDlg.filename)                     
            
        # Set styles of file dialog.
        folderDlg = ui.createFolderDialog()
        folderDlg.title = 'Fusion Folder Dialog' 
        
        # Show folder dialog
        dlgResult = folderDlg.showDialog()
        if dlgResult == adsk.core.DialogResults.DialogOK:
            msg += '\nselect folder: {}'.format(folderDlg.folder)                      
        
        ui.messageBox(msg)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))