from LogData import LogData
import os

# Folder Structure will be:
    #       <sensor type>
    #           ↳ <body location>_<data type>
    #           ↳ <body location>_<data type>
    #           ⋮
    #           ↳ <body location>_<data type>
    #       <sensor type>
    #           ↳ <body location>_<data type>
    #           ↳ <body location>_<data type>
    #           ⋮
    #           ↳ <body location>_<data type>

class SystemLogging(object):

    # Sensor Folders
    sensors =    [ 'Orientation Board', 'Chest Scale','FSR', 'IMU' ] 

    # Save standard folder name
    baseFolderName= "PSPAS_Trial"

    # Initialize SystemLogging Class Variables
    #def __init__(self):
        # Leaving Stubbed out untill we determine whether or not we require init method

    def createFolderStructure(self): 

        # Initialize values for base folder
        i = 0
        self.folderName = SystemLogging.baseFolderName + " (" + str(i) + ")"

        # Loop until unique folder value is found
        while True:
            if os.path.exists(self.folderName):
                self.folderName = SystemLogging.baseFolderName + " (" + str(i) + ")"
                i+=1
            else:   
                break

        # Make new folder for this test
        os.makedirs(self.folderName)
        # Make folder directory structure
        for sensor in SystemLogging.sensors:
            os.makedirs( os.path.join(self.folderName, sensor) )


    def parseEncoding(self, encode):
        splitData = encode.split('>')

        # Section encoded input into data types
        encode_sensorType = splitData[0]
        encode_sensorLocale = splitData[1]
        encode_dataType = splitData[2]
        encode_data = splitData[3:]

        # Initialize return variables
        sensorType = ''
        location = ''
        dataType = ''
        data = ''
    
        # Determine Sensor Type (verbose)
        if   encode_sensorType == 'OB':
            sensorType = SystemLogging.sensors[0]
        elif encode_sensorType == 'SCAL':
            sensorType = SystemLogging.sensors[1]
        elif encode_sensorType == 'FSR':
            sensorType = SystemLogging.sensors[2]
        elif encode_sensorType == 'IMU':
            sensorType = SystemLogging.sensors[3]

        # Determine Sensor Location (verbose)
        if   encode_sensorLocale == 'H':
            location = 'head'
        elif encode_sensorLocale == 'B':
            location = 'body'
        elif encode_sensorLocale == 'CH':
            location = 'chest'
        elif encode_sensorLocale == 'LR':
            location = 'leftRib'
        elif encode_sensorLocale == 'RR':
            location = 'rightRib'
        elif encode_sensorLocale == 'LF':
            location = 'leftForearm'
        elif encode_sensorLocale == 'RF':
            location = 'rightForearm'
        elif encode_sensorLocale == 'LK':
            location = 'leftKnee'
        elif encode_sensorLocale == 'RK':
            location = 'rightKnee'
        elif encode_sensorLocale == 'LL':
            location = 'leftLeg'
        elif encode_sensorLocale == 'RL':
            location = 'rightLeg'

        # Determine Data Type & Format Data based on Data TYpe (verbose)
        if   encode_dataType == 'ACC':
            dataType = 'acceleration'
            data = "x: " + encode_data[0] + ",\ty: " +  encode_data[1] + ",\tz: " + encode_data[2]
        elif encode_dataType == 'EUL':
            dataType = 'orientation'
            data = "heading: " + encode_data[0] + ",\troll: " +  encode_data[1] + ",\tpitch: " + encode_data[2]
        elif encode_dataType == 'FRC':
            dataType = 'force'
            data = "force: " + encode_data[0] 
        elif encode_dataType == 'GYR':
            dataType = 'rotation'
            data = "x: " + encode_data[0] + ",\ty: " +  encode_data[1] + ",\tz: " + encode_data[2]

        return LogData(sensorType, location, dataType, data)

    
    def populateLog(self, logData):
        # Write to folderName\sensorType\bodyLocation_dataType
        sensorType = LogData.getSensorType(logData)
        location = LogData.getLocation(logData)
        dataType = LogData.getDataType(logData)
        data = LogData.getData(logData)
    
        # sensor.txt file the input log value
        with open(os.path.join(self.folderName, sensorType,(location + "_" + dataType + ".txt")), 'a') as file:
            file.write("LOG\t" + data +"\n")


