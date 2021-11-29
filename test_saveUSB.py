import os
from SystemLogging import SystemLogging

systemLogging = SystemLogging()
SystemLogging.createFolderStructure(systemLogging)

folderName = systemLogging.getFoldername()
# Create mount-point
os.system("sudo mkdir /media/usb")

# Mount drive
os.system("sudo mount /dev/sda1 /media/usb -o uid=pi,gid=pi")

# Copy folder to usb mount-point
os.system("sudo \cp -r " + folderName + " /media/usb")

# Unmount Drive
os.system("sudo unmount /media/usb")