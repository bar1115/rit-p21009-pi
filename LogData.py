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
        """
        Override string method for object print debugging

        Returns:
            [String]: A concatenation of all LogData values
        """
        return "Sensor Type: " + self.sensorType + ", Location: " + self.location  + ", Data Type: " + self.dataType + ", Data: " + self.dataLog

    def getData(self):
        """
        Get the log Data

        Returns:
            Array []: An array of all Log Data properties
        """

        return self.sensorType, self.location, self.dataType, self.dataLog

    def getSensorType(self):
        """
        Get the log Sensor Type

        Returns:
            [String]: A string indicating the sensor type
        """
        return self.sensorType

    def getLocation(self):
        """
        Get the log sensor location

        Returns:
            [String]: A string indicating the sensors location
        """
        return self.location

    def getDataType(self):
        """
        Get the data type

        Returns:
            [String]: This indicates the unites of measurment 
                      polled form the sensor (ie Force or Acceleration)
        """
        return self.dataType
    
    def getDataLog(self):
        """
        Get the data from the sensor log (spliced)

        Returns:
            Array []: An array of each of the individual data log components
        """
        return self.dataLog

    def getDataRaw(self):
        """
         Get the data from the sensor log (not spliced)

        Returns:
            String: A String concatenation of all the individual 
                    log data measurments
        
        """
        return self.dataRaw

    def isStatusType(self):
        """
        Get the flag which indicates whether or not this LogData is a
        calibration status or log data message.

        Returns:
            [Boolean]: Status type flag
        """
        return self.status

    

