#########################################################################################
#                                                                                       # 
#   File    : SystemLogging.py                                                          # 
#   Author  : Rebecca Reich (bar1115@rit.edu)                                           # 
#   Created : ‎October ‎7, ‎2021                                                           #     
#                                                                                       # 
#   Description:                                                                        # 
#     This class is comprised of methods that handle transmission message               # 
#     processing and data storage                                                       # 
#                                                                                       # 
#        More specifically, SystemLogging includes:                                     # 
#                                                                                       # 
#             + NXP → Pi Decoding String                                                # 
#             + Pi → NXP Encoding String                                                # 
#             + Creating Folder Structures                                              # 
#             + Saving Log Data to Log File                                             # 
#             + Saving Calibration Status Data to Status File                           # 
#                                                                                       # 
#########################################################################################

from LogData import LogData
import os, datetime

# Create Encoding Value <-> File Name mapping for simplicity
# Sensor Type Maping
global SENSORS
SENSORS = {
            'OB':'Orientation Board',
            'SCAL':'Chest Scale',
            'FSR':'FSR',
            'IMU':'IMU'
            }
# Sensor Location Maping
global LOCATIONS
LOCATIONS = {
            'H':'head',
            'B':'body',
            'CH':'chest',
            'LR':'leftRib',
            'RR':'rightRib',
            'LH':'leftHip',
            'RH':'rightHip',
            'LF':'leftForearm',
            'RF':'rightForearm',
            'LK':'leftKnee',
            'RK':'rightKnee',
            'LL':'leftLeg',
            'RL':'rightLeg'
            }

global OPERATIONS
OPERATIONS = {
            'ACC':'acceleration',
            'EUL':'orientation',
            'FRC':'force',
            'GYR':'rotation',
            'LOG':'logging enabled',
            'EN':'enabled',
            'CAL':'BNO055 calibration status',
            'OFF':'offset'
            }
            
global COMMANDS
COMMANDS = {
            'OB' :   ['H', 'B'],
            'SCAL' : ['LL', 'RR'],
            'FSR' :  ['LR', 'RR', 'LH', 'RH', 'LF', 'RF', 'LK', 'RK']
           }

global start_datetime
start_datetime = datetime.datetime.now()

class SystemLogging(object):
    # Save standard folder name
    baseFolderName  = os.path.dirname(os.path.abspath(__file__)) + "/PSPAS_Logs"

    # Initialize SystemLogging Class Variables
    #def __init__(self):
        # Leaving Stubbed out untill we determine whether or not we require init method

    def createFolderStructure(self): 
        """
        Generate Folder Structure & Empty Log Files on the Pi. The folder structure is as follows:

            Folder Structure will be:
                    <sensor type>
                        ↳ <body location>_<data type>
                        ↳ <body location>_<data type>
                        ⋮
                        ↳ <body location>_<data type>
                    <sensor type>
                        ↳ <body location>_<data type>
                        ↳ <body location>_<data type>
                        ⋮
                        ↳ <body location>_<data type>

        """

        # Initialize values for base folder
        i = 0
        self.folderName = SystemLogging.baseFolderName + "_" + str(i)

        # Loop until unique folder value is found
        while True:
            if os.path.exists(self.folderName):
                self.folderName = SystemLogging.baseFolderName + "_" + str(i)
                i+=1
            else:   
                break

        # Make new folder for this test
        os.makedirs(self.folderName)
        # Make folder directory structure
        for sensor in SENSORS:
            os.makedirs( os.path.join(self.folderName, SENSORS[sensor]) )

    def getFoldername(self):
        """
        A simple get-method which retruns the foldername of this individual System Logging object
        This method is soley used in MCU_COMS to export log data to a USB

        Returns:
            [String]: The folderName for this system logging object
        """
        return self.folderName

    def encodeLogData(logData):
        """
        Revert LogData object to Encoded String

        Args:
            logData (LogData): A LogData object containing the decoded data

        Returns:
            [String]: A reverted, encoding string formatted to the input encoding

        """
        data = LogData.getDataRaw(logData)
        dataEncode = '>'.join(data)

        sensorType = LogData.getSensorType(logData)
        location = LogData.getLocation(logData)
        dataType = LogData.getDataType(logData)

        # Determine Sensor Type (short) using Type Mapping
        for st in SENSORS:
          if sensorType == SENSORS[st]:
              sensorType = st
              break

        # Determine Sensor Location (short) using Location Mapping
        for sl in LOCATIONS:
          if location == LOCATIONS[sl]:
              location = sl
              break

        # Determine Sensor Operation (short) using Location Mapping
        for so in OPERATIONS:
          if dataType == OPERATIONS[so]:
              dataType = so
              break

        return (sensorType + '>' + location + '>' + dataType  + '>' +  dataEncode)

    def populateLog(self, logData):
        """
        From an LogData object, write the log data to its corresponding file

        Args:
            logData (LogData): A LogData object containing the decoded data
        """
        # Write to folderName\sensorType\bodyLocation_dataType
        sensorType = LogData.getSensorType(logData)
        location = LogData.getLocation(logData)
        dataType = LogData.getDataType(logData)
        data = LogData.getDataLog(logData)
    
        # sensor.txt file the input log value
        with open(os.path.join(self.folderName, sensorType,(location + "_" + dataType + ".txt")), 'a') as file:
            now = datetime.datetime.now()
            normalized = now - datetime.timedelta(hours=start_datetime.hour, minutes=start_datetime.minute)
            stamp = normalized.strftime("[%H:%M:%S.%f] ")
            file.write(stamp + data + "\n")


    def populateStatus(self, logData):
        """
        Populates the calibration status data into the CALIBRATION_PRESETS.txt file

        Args:
            logData (LogData): A LogData object containing the decoded data
        """
        # Write to folderName\'CALIBRATION_PRESETS.txt'
        encode = SystemLogging.encodeLogData(logData)
    
        with open("CALIBRATION_PRESETS.txt", 'a') as file:
            file.write(encode +"\n")


    def parseEncoding(encode):
        """
        Parses an encoded string recieved from the NXP and converts it to a logData object for easy handling 

        Args:
            encode (String): An encoded string recieved from the NXP to the Pi

        Returns:
            [logData] : A LogData object containing the decoded data
        """
        splitData = encode.split('>')

        # Section encoded input into data types
        if (len(splitData) <= 3):
            return None

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
        for st in SENSORS:
          if encode_sensorType == st:
              sensorType = SENSORS[st]
              break
        
        # Invalid Encodding - Return None and handle outside
        if sensorType == '':
            return None

        for sl in LOCATIONS:
          if encode_sensorLocale == sl:
              location = LOCATIONS[sl]
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
            # Invalid Encoding - Return None and handle outside
            return None

        return LogData( sensorType=sensorType, location=location, dataType=dataType, dataLog=data, dataRaw=encode_data, status=status)


    def generateEncoding( logData ):
        """
        Converts a logData object into an encoded string much like the ones recieved from the NXP

        Args:
            logData (LogData): A LogData object containing the decoded data

        Returns:
            encode (String): An encoded string recieved from the NXP to the Pi
        """

        encodedString = ''
        encodeData = ''

        # Section encoded input into data types
        sensorType = LogData.getSensorType(logData)
        location = LogData.getLocation(logData)
        dataType = LogData.getDataType(logData)
        data = LogData.getData(logData)

        # Determine Sensor Type (verbose) using Type Mapping
        for st in SENSORS.values():
          if sensorType == st:
              sensorType += st

        # Determine Sensor Location (verbose) using Location Mapping
        for sl in LOCATIONS.values():
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
            if (len(splitData) < 3):
                return "ERROR"
            else:
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
            if (len(splitData) < 3):
                return "ERROR"
            else:
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
            if (len(splitData) < 3):
                return "ERROR"
            else:
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
            if (len(splitData) < 4):
                return "ERROR"
            else:
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
                if (len(splitData) < 3):
                    return "ERROR"
                else:
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

