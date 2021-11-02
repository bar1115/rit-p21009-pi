from SystemLogging import SystemLogging

# Initialize a SystemLogging variable
testSysLog = SystemLogging()

# Create the folder structure
SystemLogging.createFolderStructure(testSysLog)

# Create random encodings for all sensor cases
# Data Encodings
testParseEncode0 = SystemLogging.parseEncoding("OB>H>ACC>1234>4567>78910")
print(testParseEncode0)
testParseEncode1 = SystemLogging.parseEncoding("OB>H>EUL>10987>7654>4321")
print(testParseEncode1)
testParseEncode2 = SystemLogging.parseEncoding("OB>B>ACC>ABC>EFG>HIJ")
print(testParseEncode2)
testParseEncode3 = SystemLogging.parseEncoding("SCAL>CH>FRC>40404040404")
print(testParseEncode3)
# testParseEncode4 = SystemLogging.parseEncoding("FSR>LR>FRC>12345678910")
# print(testParseEncode4)
# testParseEncode5 = SystemLogging.parseEncoding("FSR>RR>FRC>12345678910")
# print(testParseEncode5)
# testParseEncode6 = SystemLogging.parseEncoding("FSR>LF>FRC>12345678910")
# print(testParseEncode6)
# testParseEncode7 = SystemLogging.parseEncoding("IMU>LL>ACC>ABC>ABC>ABC")
# print(testParseEncode7)
# testParseEncode8 = SystemLogging.parseEncoding("IMU>LL>GYR>ABC>ABC>ABC")
# print(testParseEncode8)
# testParseEncode9 = SystemLogging.parseEncoding("IMU>RL>ACC>ABC>ABC>ABC")
# print(testParseEncode9)
# testParseEncode10 = SystemLogging.parseEncoding("IMU>RL>GYR>ABC>ABC>ABC")
# print(testParseEncode10)

# Status Encodings
testParseEncode11 = SystemLogging.parseEncoding("SCAL>CH>EN>1")
print(testParseEncode11)
testParseEncode12 = SystemLogging.parseEncoding("OB>H>CAL>1>2>3>4")
print(testParseEncode12)
testParseEncode13 = SystemLogging.parseEncoding("SCAL>CH>EN>321")
print(testParseEncode13)

# Loop 1000 and populate each sensor type with faux encoding
for i in range(0, 1000):
    SystemLogging.populateLog( testSysLog, testParseEncode0)

for i in range(0, 1000):
    SystemLogging.populateLog( testSysLog, testParseEncode1)

for i in range(0, 1000):
    SystemLogging.populateLog( testSysLog, testParseEncode2)

for i in range(0, 1000):
    SystemLogging.populateLog( testSysLog, testParseEncode3)

# for i in range(0, 1000):
#     SystemLogging.populateLog( testSysLog, testParseEncode4)

# for i in range(0, 1000):
#     SystemLogging.populateLog( testSysLog, testParseEncode5)

# for i in range(0, 1000):
#     SystemLogging.populateLog( testSysLog, testParseEncode6)

# for i in range(0, 1000):
#     SystemLogging.populateLog( testSysLog, testParseEncode7)

# for i in range(0, 1000):
#     SystemLogging.populateLog( testSysLog, testParseEncode8)

# for i in range(0, 1000):
#     SystemLogging.populateLog( testSysLog, testParseEncode9)

# for i in range(0, 1000):
#     SystemLogging.populateLog( testSysLog, testParseEncode10)

for i in range(0, 100):
    SystemLogging.populateStatus( testSysLog, testParseEncode11)

for i in range(0, 100):
    SystemLogging.populateStatus( testSysLog, testParseEncode12)

for i in range(0, 100):
    SystemLogging.populateStatus( testSysLog, testParseEncode13)