#########################################################################################
#                                                                                       #
#   File    : UART_Comms.py                                                             #
#   Author  : Rebecca Reich (bar1115@rit.edu)                                           #
#   Created : October ‎19, ‎2021                                                          #
#                                                                                       #
#   Description:                                                                        #
#     Main program entry point for RIT MSD Team P21009 Raspberry Pi software.
#     NXT FRDM-K64F MCU target.
#                                                                                       #
#########################################################################################

from SystemLogging import SystemLogging
from ControlPanelGUI import ControlPanelGUI
import os
import serial, time

# Establish Serial Connection to TTYS0
serialport = serial.Serial("/dev/ttyS0", baudrate=576000, timeout=0.1)

# Create System Logging Object & Create Folder Structure
systemLogging = SystemLogging()
SystemLogging.createFolderStructure(systemLogging)


# On startup, send stored Calibration data over to NXP
# Sleep for 5s to wait for bootup
time.sleep(5)
with open("CALIBRATION_PRESETS.txt", 'r') as calPresets:
    for cp in calPresets:
        serialport.write(cp)

# Begin Control-Loop Main Method
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
                print("Malformed Encoding Encountered - Ignore Data")
                break

            # Write to file
            SystemLogging.populateLog( systemLogging, parsedEncoding)

            break

        except ValueError:
            # Byte String malformed
            print("Malformed Byte String Encountered - Ignore Data")








    # serialport.write("rnSay something:")
    #     rcv = port.read(10)
    #     serialport.write("rnYou sent:" + repr(rcv))