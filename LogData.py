#########################################################################################
#                                                                                       #
#   File    : LogData.py                                                                #
#   Author  : Rebecca Reich (bar1115@rit.edu)                                           #
#   Created : ‎October ‎7, ‎2021                                                           #    
#                                                                                       #
#   Description:                                                                        #
#     A Log Data object which contains the individual parsed data values that           #
#     were collected from NXP transmission. More specifically, it contains the          #
#     verbose namings/values to each component of the encoding.                         #   
#                                                                                       #
#########################################################################################

class LogData(object):

    # Overloaded Constructor
    #   - If no values are input, the LogData properties are 'None' 
    def __init__(self, sensorType = None, location = None, dataType = None, dataLog = None, dataRaw = None, status = False):

        self.sensorType = sensorType
        self.location = location
        self.dataType = dataType
        self.dataLog = dataLog
        self.dataRaw = dataRaw
        self.status = status

    def __str__(self):
        return "Sensor Type: " + self.sensorType + ", Location: " + self.location  + ", Data Type: " + self.dataType + ", Data: " + self.dataLog

    def getData(self):
        return self.sensorType, self.location, self.dataType, self.dataLog

    def getSensorType(self):
        return self.sensorType

    def getLocation(self):
        return self.location

    def getDataType(self):
        return self.dataType
    
    def getDataLog(self):
        return self.dataLog

    def getDataRaw(self):
        return self.dataRaw

    def isStatusType(self):
        return self.status

    

