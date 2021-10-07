

class LogData(object):

    def __init__(self, sensorType, location, dataType, data):

        self.sensorType = sensorType
        self.location = location
        self.dataType = dataType
        self.data = data

    def __str__(self):
        return "Sensor Type: " + self.sensorType + ", Location: " + self.location  + ", Data Type: " + self.dataType + ", Data: " + self.data

    def getData(self):
        return self.sensorType, self.location, self.dataType, self.data

    def getSensorType(self):
        return self.sensorType

    def getLocation(self):
        return self.location

    def getDataType(self):
        return self.dataType
    
    def getData(self):
        return self.data

    

