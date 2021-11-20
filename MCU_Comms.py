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

import serial, socket, time
from SystemLogging import SystemLogging


class MCU_Comms():

    # Constants
    #SERIAL_PORT     = "/dev/ttyS0"
    SERIAL_PORT     = "COM12"
    SERIAL_BAUD     = 576000
    SERIAL_TIMEOUT  = 0.1
    ETHERNET_IP     = "169.254.108.19"
    ETHERNET_PORT   = 37
    MAX_STR_LENGTH  = 256


    def __init__(self):
        # Establish UART connection to SERIAL_PORT
        global uart
        uart = serial.Serial(self.SERIAL_PORT, baudrate=self.SERIAL_BAUD, timeout=self.SERIAL_TIMEOUT)

        # Establish Ethernet connection via UDP server socket
        # global ethernet
        # ethernet = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # ethernet.bind((self.ETHERNET_IP, self.ETHERNET_PORT))
        
        # Create System Logging Object & Create Folder Structure
        global systemLogging 
        systemLogging = SystemLogging()
        SystemLogging.createFolderStructure(systemLogging)

        # Sleep for 5s to wait for MCU to bootup and initialize
        time.sleep(5)

        # On startup, send stored presets over to MCU
        with open("PRESETS.txt", 'r') as file:
            for line in file:
                uart.write(line.encode())

                
    def poll_data(self, enable):
        """
        Polls for data from the MCU via the Ethernet connection.

        Args:
            enable: An enable function that returns a boolean indicating if the thread execution should continue.

        Returns:
            None
        """

        while enable():
            # # TODO: Read incoming Ethernet data
            # rcv = ethernet.recvfrom(self.MAX_STR_LENGTH)

            # # Try to decode the message.
            # try:
            #     # Byte String properly formed & decoded
            #     str = rcv.decode() 
            #     # Filter out miscellaneous characters that may exist at the end of the packet.
            #     str = str[:len(str)-1]
            #     # Since its properly recieved, process and save encoding accordingly
            #     parsedEncoding = SystemLogging.parseEncoding(str)
            #     # Error Check that encoding was properly formatted
            #     if parsedEncoding != None:
            #         # Write to file
            #         SystemLogging.populateLog(systemLogging, parsedEncoding)                        

            # # Cannot recieve byte string
            # except ValueError:
            #     # Byte String malformed
            #     print("WARNING: poll_data Malformed Byte String Encountered - Ignoring Data")

            print("poll_data thread!")
            time.sleep(1)

                
    def poll_status(self, enable):
        """
        Polls for status updates from the MCU via the UART serial connection.

        Args:
            enable: An enable function that returns a boolean indicating if the thread execution should continue.

        Returns:
            None
        """

        while enable():
            # # Read incoming UART data until either MAX_STR_LENGTH bytes received or LF encountered
            # rcv = uart.read_until(size=self.MAX_STR_LENGTH)

            # # Was message recieved?
            # if rcv:
            #     # Try to decode the message.
            #     try:
            #         # Byte String properly formed & decoded
            #         str = rcv.strip().decode() 
            #         # Since its properly recieved, process and save encoding accordingly
            #         parsedEncoding = SystemLogging.parseEncoding(str)
            #         # Error Check that encoding was properly formatted
            #         if parsedEncoding != None and parsedEncoding.status:
            #             # TODO: handle status
            #             placeholder = 1

            #     # Cannot recieve byte string
            #     except ValueError:
            #         # Byte String malformed
            #         print("WARNING: poll_status Malformed Byte String Encountered - Ignoring Data")

            print("poll_status thread!")
            time.sleep(1)
