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

import os
import tkinter as tk
import serial, time, threading, ctypes


class UART_Comms(threading.Thread):

    serialName = "/dev/ttyS0"
    baud = 576000
    time = 0.1

    def __init__(self):
        # Initialize this object as a thread
        # threading.Thread.__init__(self)

        # Establish Serial Connection to TTYS0
        global serialport 
        serialport = serial.Serial("/dev/ttyS0", baudrate=576000, timeout=0.1)
        
        # Create System Logging Object & Create Folder Structure
        global systemLogging 
        systemLogging = SystemLogging()
        SystemLogging.createFolderStructure(systemLogging)

        # On startup, send stored Calibration data over to NXP
        # Sleep for 5s to wait for bootup
        time.sleep(5)
        with open("CALIBRATION_PRESETS.txt", 'r') as calPresets:
            for cp in calPresets:
                serialport.write(cp)

    #def run(self):
    def poll_data(self):

        # USE Try/Finally Exception Block to run Serial Comm Thread

        # Continuously run until raise_exception is called to terminate thread
        try:
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

                        # Write to file
                        SystemLogging.populateLog( systemLogging, parsedEncoding)

                    # Cannot recieve byte string
                    except ValueError:
                        # Byte String malformed
                        print("Malformed Byte String Encountered - Ignore Data")

        # Exception was thrown. Terminate thread and close serial connection
        finally:
            # TODO end serial connection
            print('stop testing')

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure to terminate thread')

            

# if __name__ == "__main__":
#     root = tk.Tk()
#     gui_thread = ControlPanelGUI(root)
#     main_thread = UART_Comms()
#     root.mainloop()


   

















