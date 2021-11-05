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

    # Create Encoding Value <-> File Name mapping for simplicity
    # Sensor Type Maping
    sensors = {
                    'OB':'Orientation Board',
                    'SCAL':'Chest Scale',
                    'FSR':'FSR',
                    'IMU':'IMU'
                 }
    # Sensor Location Maping
    locations = {
                    'H':'head',
                    'B':'body',
                    'CH':'chest',
                    'LR':'leftRib',
                    'RR':'rightRib',
                    'LF':'leftForearm',
                    'RF':'rightForearm',
                    'LK':'leftKnee',
                    'RK':'rightKnee',
                    'LL':'leftLeg',
                    'RL':'rightLeg'
                 }

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
            os.makedirs( os.path.join(self.folderName, SystemLogging.sensors[sensor]) )

    def encodeLogData(logData):
        data = LogData.getDataRaw(logData)
        dataEncode = '>'.join(data)

        sensorType = LogData.getSensorType(logData)
        location = LogData.getLocation(logData)
        dataType = LogData.getDataType(logData)

        # Determine Sensor Type (verbose) using Type Mapping
        for st in SystemLogging.sensors:
          if sensorType == SystemLogging.sensors[st]:
              sensorType = st
              break

        # Determine Sensor Location (verbose) using Location Mapping
        for sl in SystemLogging.locations:
          if location == SystemLogging.locations[sl]:
              location = sl
              break

        return (sensorType + '>' + location + '>' + dataType  + '>' +  dataEncode)

    def populateLog(self, logData):
        # Write to folderName\sensorType\bodyLocation_dataType
        sensorType = LogData.getSensorType(logData)
        location = LogData.getLocation(logData)
        dataType = LogData.getDataType(logData)
        data = LogData.getDataLog(logData)
    
        # sensor.txt file the input log value
        with open(os.path.join(self.folderName, sensorType,(location + "_" + dataType + ".txt")), 'a') as file:
            file.write("LOG\t" + data +"\n")


    def populateStatus(self, logData):
        # Write to folderName\'STATUS.txt'
        encode = SystemLogging.encodeLogData(logData)
    
        with open(os.path.join(self.folderName, "STATUS.txt"), 'a') as file:
            file.write(encode +"\n")


    def parseEncoding(encode):
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
        status = False
    
        # Determine Sensor Type (verbose) using Type Mapping
        for st in SystemLogging.sensors:
          if encode_sensorType == st:
              sensorType = SystemLogging.sensors[st]
              break
        
        # Invalid Encodding - Return None and handle outside
        if sensorType == '':
            return None

        # Determine Sensor Location (verbose) using Location Mapping
        for sl in SystemLogging.locations:
          if encode_sensorLocale == sl:
              location = SystemLogging.locations[sl]
              break

        # Invalid Encodding - Return None and handle outside
        if location == '':
            return None

        # Determine Data Type and Format Data based on Data Type/Statuses; If status type, set status flag (verbose)
        # DATA TYPE
        encode_dataSize = len(encode_data)

        if   (encode_dataType == 'ACC') and (encode_dataSize == 3):
            dataType = 'acceleration'
            data = "x: " + encode_data[0] + ",\ty: " +  encode_data[1] + ",\tz: " + encode_data[2]
        elif (encode_dataType == 'EUL') and (encode_dataSize == 3):
            dataType = 'orientation'
            data = "heading: " + encode_data[0] + ",\troll: " +  encode_data[1] + ",\tpitch: " + encode_data[2]
        elif (encode_dataType == 'FRC') and (encode_dataSize == 1):
            dataType = 'force'
            data = "force: " + encode_data[0] 
        elif (encode_dataType == 'GYR') and (encode_dataSize == 3):
            dataType = 'rotation'
            data = "x: " + encode_data[0] + ",\ty: " +  encode_data[1] + ",\tz: " + encode_data[2]
        # STATUSES
        elif (encode_dataType == 'LOG') and (encode_dataSize == 1):
            status = True
            dataType = 'logging enabled'
            data = "Enable: " + encode_data[0]
        elif (encode_dataType == 'EN') and (encode_dataSize == 1):
            status = True
            dataType = 'enabled'
            data = "Enable: " + encode_data[0]
        elif (encode_dataType == 'CAL') and (encode_dataSize == 4):
            status = True
            dataType = 'BNO055 calibration status'
            data = "GYR: " + encode_data[0] + ",\tACC: " +  encode_data[1] + ",\tMAG: " + encode_data[2] + ",\SYS: " + encode_data[3]
        elif (encode_dataType == 'OFF') and (encode_dataSize == 3):
            status = True
            dataType = 'offset'
            data = "GYR: " + encode_data[0] + ",\tACC: " +  encode_data[1] + ",\tMAG: " + encode_data[2]
        else:
            # Invalid Encodding - Return None and handle outside
            return None

        return LogData( sensorType=sensorType, location=location, dataType=dataType, dataLog=data, dataRaw=encode_data, status=status)


    def generateEncoding( logData ):

        encodedString = ''
        encodeData = ''

        # Section encoded input into data types
        sensorType = LogData.getSensorType(logData)
        location = LogData.getLocation(logData)
        dataType = LogData.getDataType(logData)
        data = LogData.getData(logData)

        # Determine Sensor Type (verbose) using Type Mapping
        for st in SystemLogging.sensors.values():
          if sensorType == st:
              sensorType += st

        # Determine Sensor Location (verbose) using Location Mapping
        for sl in SystemLogging.locations.values():
          if sensorType == sl:
              location += sl

        # Add deliminitor
        encodedString += '>'

        # Determine Data Type and Format Data based on Data TYpe (encoded)
        if   dataType == 'acceleration':
            encodedString += 'ACC'

            # Add deliminitor
            encodedString += '>'
            
            # Determine individual data value from string
            splitData = data.split(',\t')
            d1 = splitData[0][3:]
            d2 = splitData[1][3:]
            d3 = splitData[2][3:]

            encodedString +=  ( d1 + '>' + d2 + '>' + d3 )

        elif dataType == 'orientation':
            encodedString += 'EUL'

            # Add deliminitor
            encodedString += '>'
            
            # Determine individual data value from string
            splitData = data.split(',\t')
            d1 = splitData[0][9:]
            d2 = splitData[1][6:]
            d3 = splitData[2][7:]

            encodedString +=  ( d1 + '>' + d2 + '>' + d3 )
            
        elif dataType == 'force':
            encodedString += 'FRC'

            # Add deliminitor
            encodedString += '>'
            encodedString += data.split(': ')[1] 

        elif dataType == 'rotation':
            encodedString += 'GYR'

            # Add deliminitor
            encodedString += '>'
            
            # Determine individual data value from string
            splitData = data.split(',\t')
            d1 = splitData[0][3:]
            d2 = splitData[1][3:]
            d3 = splitData[2][3:]

            encodedString +=  ( d1 + '>' + d2 + '>' + d3 )

        elif dataType == 'logging enabled':
            encodedString += 'LOG'

            # Add deliminitor
            encodedString += '>'
            encodedString += data.split(': ')[1] 

        elif dataType == 'enabled':
            encodedString += 'EN'

            # Add deliminitor
            encodedString += '>'
            encodedString += data.split(': ')[1] 

        elif dataType == 'BNO055 calibration status':
            encodedString += 'CAL'

            # Add deliminitor
            encodedString += '>'
            
            # Determine individual data value from string
            splitData = data.split(',\t')
            d1 = splitData[0][3:]
            d2 = splitData[1][3:]
            d3 = splitData[2][3:]
            d4 = splitData[3][3:]

            encodedString +=  ( d1 + '>' + d2 + '>' + d3 + '>' + d4 )
        
        elif dataType == 'offset':
            encodedString += 'OFF'

            # Add deliminitor
            encodedString += '>'
            
            if sensorType == 'OB':
                # Determine individual data value from string
                splitData = data.split(',\t')
                d1 = splitData[0][3:]
                d2 = splitData[1][3:]
                d3 = splitData[2][3:]

                encodedString +=  ( d1 + '>' + d2 + '>' + d3 )

            if sensorType == 'SCAL':
                encodedString += data.split(': ')[1] 

        else:
            # Invalid Encodding - Return None and handle outside
            return ''

        encodedString += '\n'

        return encodedString

