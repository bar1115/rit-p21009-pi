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

class SystemLogging:

    # Sensor Folders
    sensors =    [ 'Orientation Board', 'Chest Scale','FSR', 'IMU' ] 

    sensorType = ''
    location = ''
    dataType = ''
    data = ''


    # Initialize SystemLogging Class Variables
    def __init__(self):
        # Initialize values for base folder
        i = 0
        baseFolderName= "PSPAS_Trial"
        self.folderName = baseFolderName + " (" + i + ")"


    def createFolderStructrue(self): 

        # Loop until unique folder value is found
        while True:
            if os.path.exists(self.folderName):
                self.folderName = baseFolderName + " (" + i + ")"
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
        encode_dataType = splitData[1]
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
        elif encode_dataType == 'FSR':
            sensorType = SystemLogging.sensors[2]
        elif encode_dataType == 'IMU':
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
            data = "x: " + encode_data[0] + ", y: " +  encode_data[1] + ", z: " + encode_data[2]
        elif encode_dataType == 'EUL':
            dataType = 'orientation'
            data = "heading: " + encode_data[0] + ", roll: " +  encode_data[1] + ", pitch: " + encode_data[2]
        elif encode_dataType == 'FRC':
            dataType = 'force'
            data = "force: " + encode_data[0] 
        elif encode_dataType == 'GYR':
            dataType = 'rotation'
            data = "x: " + encode_data[0] + ", y: " +  encode_data[1] + ", z: " + encode_data[2]

        return sensorType, location, dataType, data

    
    def populateLog(self, sensorType, location, dataType, data):
        # Write to folderName\sensorType\bodyLocation_dataType
        # 
        # sensor.txt file the input log value
        with open(os.path.join(self.folderName, sensorType,(location + "_" + dataType)), 'a') as file:
            file.write("LOG\t" + data +"\n")


