import machine
import utime
import fileinput

#Script Begins by Reading Lines of the Cal.txt file. As a calibration file, there should only be 1 measurement for each sensor.
calfile = open("cal.txt")

for line in calfile.readlines():
    if line.find('OB::ACC:: ') == 1:
        OrientationAccRef = line
    elif line.find('IMU::ACC::  ') == 1:
        IMUAccRef = line
    elif line.find('IMU::GYR::  ') == 1:
        IMUGyrRef = line
    else:
        continue

calfile.close()

#Script Proceeds to open the current log file (as retrieved from the NXP) and also create a "report.txt" file
logfile = open("log.txt","r") #The Raspberry Pi will expect a file named log.txt from the NXG
reportFile = open("report.txt","w")

for line in logfile.readlines():
    if line.find('OB::ACC:: ') == 1:
        OrientationAccCur = line - OrientationAccRef
        reportFile.write(OrientationAccCur + "\n")
        convertUnits(OrientationAccCur, 'Acceleration')
        sendToUI(OrientationAccCur)
    elif line.find('IMU::ACC:: ') == 1:
        IMUAccCur = line - IMUAccRef
        reportFile.write(IMUAccCur + "\n")
        convertUnits(IMUAccCur, 'Acceleration')
        sendToUI(OrientationAccCur)
    elif line.find('IMU::GYR:: ') == 1:
        IMUGyrCur = line - IMUGyrRef
        reportFile.write(IMUGyrCur + "\n")
        convertUnits(IMUGyrCur, 'Gyroscope')
        sendToUI(OrientationAccCur)

logfile.close()