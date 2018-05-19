#Author-
#Description-

"""Test of Data management API
Show all the projects, folders and files in the active hub.
http://adndevblog.typepad.com/technology_perspective/2017/06/relationship-between-fusion-360-api-and-data-management-api.html
"""

import os
import time
import adsk.core, adsk.fusion, adsk.cam, traceback


def run(context):
    st = time.time()
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface        
        hub = app.data.activeHub

        summary = '\nActive Hub = ' + hub.name
#        summary += summary + '\nHub.id = ' + hub.id
         
        projects = hub.dataProjects
        for index in range(0, projects.count):
            project = projects.item(index)
            summary += "\n\nProject = " + project.name
            #summary += "\n\nProject.id = " + project.id
          
            folder = project.rootFolder
            summary += "\n\n\tRoot Folder = " + folder.name
            summary += "\n\tRoot Folder.id = " + folder.id
            
            files = folder.dataFiles
            
            for index in range(0, files.count):
                file = files.item(index)
                summary += "\n\n\t\tFile = " + file.name
                summary += "\n\t\tFile.id = " + file.id
            
            folders = project.rootFolder.dataFolders
            for index in range(0, folders.count):
                folder = folders.item(index)
                summary += "\n\n\t\tFolder = " + folder.name
                summary += "\n\t\tFolder.id = " + folder.id
                files = folder.dataFiles
                for index in range(0, files.count):
                    file = files.item(index)
                    summary += "\n\n\t\t\tFile = " + file.name
                    summary += "\n\t\t\tFile.id = " + file.id
                    summary += "\n\t\t\tFile.ObjectType = " + file.objectType
                    summary += "\n\t\t\tFile.fileExtension = " + file.fileExtension
                    
#        ui.messageBox(summary) # This is not recommended because the messageBox will be too high to read the whole message in.
        outputPath = os.path.join(os.environ.get('USERPROFILE'), "Downloads", "output.txt")
        with open(outputPath, "w") as ff:
            ff.write(summary)
        print(summary)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
    
    print("Elapsed time: {0:.2f}".format(time.time() - st))