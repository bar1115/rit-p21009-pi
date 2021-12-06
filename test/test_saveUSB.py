import os
from SystemLogging import SystemLogging

systemLogging = SystemLogging()
SystemLogging.createFolderStructure(systemLogging)

folderName = systemLogging.getFoldername()
baseFolderName = folderName
i = 0

# Copy folder to usb mount-point
while True:
            if os.path.exists(folderName):
                folderName = baseFolderName + " " + str(i)
                i+=1
            else:   
                break

os.system("sudo \cp -r " + folderName + " /media/usb")
