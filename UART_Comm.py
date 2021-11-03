from SystemLogging import SystemLogging
import os
import serial, datetime

# Establish Serial Connection to TTYS0
serialport = serial.Serial("/dev/ttyS0", baudrate=576000, timeout=0.1)

# Create System Logging Object & Create Folder Structure
systemLogging = SystemLogging()
SystemLogging.createFolderStructure(systemLogging)

while True:
    # Establish Serial Port Connection to UART TTYS0
    # Read until a given byte string of 256B is encountered
    rcv = serialport.read_until(size=256)

    # Was an msg recieved?
    if (rcv):
        # Attempt to recieve a byte string encoding from the NXP
        try:
            # Byte String properly formed & decoded
            encode = rcv.strip().decode() 

            # Since its properly recieved, process and save encoding accordingly
            # Decode Message
            parsedEncoding = SystemLogging.parseEncoding(encode)

            # Error Check that encoding was properly formatted
            if parsedEncoding == None:
                # Incorrectly formatted; break and dont process further
                break

            # Write to file
            SystemLogging.populateLog( systemLogging, parsedEncoding)

            break

        except ValueError:
            # Byte String malformed
            print("Oops!  That was no valid number.  Try again")








    # serialport.write("rnSay something:")
    #     rcv = port.read(10)
    #     serialport.write("rnYou sent:" + repr(rcv))