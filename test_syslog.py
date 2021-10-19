from SystemLogging import SystemLogging

# Initialize a SystemLogging variable
testSysLog = SystemLogging()

# Create the folder structure
SystemLogging.createFolderStructure(testSysLog)

# Create random encodings for all sensor cases
testParseEncode0 = SystemLogging.parseEncoding("OB>H>ACC>1234>4567>78910")

print()
print(testParseEncode0)

print()

unincodeTest = SystemLogging.generateEncoding(testParseEncode0)
print("OB>H>ACC>1234>4567>78910\n"+unincodeTest)

# testParseEncode1 = SystemLogging.parseEncoding(testSysLog, "OB>H>EUL>10987>7654>4321")
# print(testParseEncode1)
# testParseEncode2 = SystemLogging.parseEncoding(testSysLog, "OB>B>ACC>ABC>EFG>HIJ")
# print(testParseEncode2)
# testParseEncode3 = SystemLogging.parseEncoding(testSysLog, "SCAL>CH>FRC>40404040404")
# print(testParseEncode3)
# testParseEncode4 = SystemLogging.parseEncoding(testSysLog, "FSR>LR>FRC>12345678910")
# print(testParseEncode4)
# testParseEncode5 = SystemLogging.parseEncoding(testSysLog, "FSR>RR>FRC>12345678910")
# print(testParseEncode5)
# testParseEncode6 = SystemLogging.parseEncoding(testSysLog, "FSR>LF>FRC>12345678910")
# print(testParseEncode6)
# testParseEncode7 = SystemLogging.parseEncoding(testSysLog, "IMU>LL>ACC>ABC>ABC>ABC")
# print(testParseEncode7)
# testParseEncode8 = SystemLogging.parseEncoding(testSysLog, "IMU>LL>GYR>ABC>ABC>ABC")
# print(testParseEncode8)
# testParseEncode9 = SystemLogging.parseEncoding(testSysLog, "IMU>RL>ACC>ABC>ABC>ABC")
# print(testParseEncode9)
# testParseEncode10 = SystemLogging.parseEncoding(testSysLog, "IMU>RL>GYR>ABC>ABC>ABC")
# print(testParseEncode10)

# Loop 1000 and populate each sensor type with faux encoding
# for i in range(0, 1000):
#     SystemLogging.populateLog( testSysLog, testParseEncode0)

# for i in range(0, 1000):
#     SystemLogging.populateLog( testSysLog, testParseEncode1)

# for i in range(0, 1000):
#     SystemLogging.populateLog( testSysLog, testParseEncode2)

# for i in range(0, 1000):
#     SystemLogging.populateLog( testSysLog, testParseEncode3)

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