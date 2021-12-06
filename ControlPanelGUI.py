#########################################################################################
#                                                                                       #
#   File    : ControlPanelGUI.py                                                        #
#   Author  : Rebecca Reich (bar1115@rit.edu) & Thomas Sosa (ts5630@rit.edu) &          #
#   Created : ‎October ‎7, ‎2021                                                           #    
#                                                                                       #
#   Description:                                                                        #
#     The Control Panel GUI, which creates the labels, buttons and button events        #   
#     graphics on the systems touch-logoLabel controller. This will run as a thread     #
#     in order to parallelize its functionality with the main control loop              #
#                                                                                       #
#########################################################################################

import threading, os
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from PIL import Image, ImageTk

from MCU_Comms import MCU_Comms


class ControlPanelGUI(threading.Thread):

    WIDTH       = 480
    HEIGHT      = 320
    GRID_DIM    = 6
    DIR         = os.path.dirname(os.path.abspath(__file__)) 
    
    def __init__(self, root):
        """
        Initialize the Buttons and Label graphics

        Args:
            root (Tk): The tkinter object necessary to estable layout
        """

        # Setup root
        self.root = root
        self.root.title("Pediactric Test Mannequin")

        # Initialize GUI thread
        threading.Thread.__init__(self)

        # Setting - Window Size
        ControlPanelGUI.highlightColor = "#85d3e9"
        ControlPanelGUI.grayColor = "#ccc"
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (self.WIDTH, self.HEIGHT, (screenwidth - self.WIDTH) / 2, (screenheight - self.HEIGHT) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)
        ft = tkFont.Font(family='Times',size=10)

        # Create a grid GRID_DIM x GRID_DIM
        for rows in range(0, ControlPanelGUI.GRID_DIM - 1):
            self.root.rowconfigure(rows, weight=1)
            self.root.columnconfigure(rows,weight=1)

        # Initialize communications to the MCU
        self.mcuComms = MCU_Comms()
        self.collect_en = False

        # Initialize device enables.
        self.obEnFlag = True
        self.scaleEnFlag = True
        self.fsrEnFlag = True
        self.imuEnFlag = True
            
        self.start()
    

    def run(self):
        """
        Begin the GUI starting with the bootScreen. This is nescessary for
        threadding.
        """
        self.bootScreen()


    def clearGrid(self):
        """
        The GUI is formatted within a 6x6 grid. In order to change screen menues, the
        grid is cleared and repopulated with the following screens widgits.
        This method is what does the clearing.
        """
        # Clear all elements in the window
        for widget in self.root.winfo_children():
            widget.destroy()


    def createEnButton(self, root, r, c, sensor, type):
        """
        Create the EN button for the Calibration Menue. This simplifies the
        populating the calibration menue

        Args:
            root (Tk): The tkinter object necessary to estable layout
            r (int): Interger representing the grid-row
            c (int): Interger representing the grid-column
            sensor (String): Sensor's Name
            type (String): Sensor's Type
        """

        enButton=tk.Button(root, height=3, width=20)
        enButton["bg"] = ControlPanelGUI.highlightColor
        enButton["font"] = tkFont.Font(family='Helvetica', size=12)
        enButton["text"] = "DISABLE"
        enButton.grid(row = r, column = c, sticky='n', padx=10, ipady=10)
        enButton["command"] = lambda: self.enSensor(sensor, type, enButton)


    def createZeroButton(self, root, r, c, sensor, type):
        """
        Create the ZERO button for the Calibration Menue. This simplifies the
        populating the calibration menue

        Args:
            root (Tk): The tkinter object necessary to estable layout
            r (int): Interger representing the grid-row
            c (int): Interger representing the grid-column
            sensor (String): Sensor's Name
            type (String): Sensor's Type
        """

        zeroButton=tk.Button(root, height=3, width=20)
        zeroButton["bg"] = ControlPanelGUI.highlightColor
        zeroButton["font"] = tkFont.Font(family='Helvetica', size=12)
        zeroButton["text"] = "ZERO"
        zeroButton.grid(row = r, column = c, sticky='n', padx=10, pady=20, ipady=10)
        zeroButton["command"] = lambda: self.zeroSensor(sensor, type)


    def bootScreen( self ):
        """
        Populate the grid with the BOOT SCREEN 

        """

        self.root.title("BOOT MENU")

        logo = Image.open(self.DIR + "/icons/logo.png")
        logo = logo.resize((140, 50), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(logo)
        logoLabel = Label(self.root, image=logo)
        logoLabel.image = logo
        logoLabel.grid(row = 0, column = 0, padx=10, sticky='w', columnspan=2)

        nameLabel=tk.Label(self.root)
        nameLabel["font"] = tkFont.Font(family='Helvetica', weight="bold", size=14)
        nameLabel["fg"] = "#000000"
        nameLabel["justify"] = "center"
        nameLabel["text"] = "PSPAS Home"
        nameLabel.grid(row = 0, padx=10, pady=30, sticky='w', column = 3, columnspan = 2)

        confMenuButton=tk.Button(self.root, height=5, width=15)
        confMenuButton["bg"] = ControlPanelGUI.highlightColor
        confMenuButton["font"] = tkFont.Font(family='Helvetica', size=12)
        confMenuButton["fg"] = "#000000"
        confMenuButton["justify"] = "center"
        confMenuButton["text"] = "Configure\nMenu"
        confMenuButton.grid(row = 2, sticky='n', padx=10, column = 0, columnspan=2, rowspan=2)
        confMenuButton["command"] = self.loadConfigureMenu

        collectButton=tk.Button(self.root, height=5, width=15)
        collectButton["bg"] = ControlPanelGUI.highlightColor
        collectButton["font"] = tkFont.Font(family='Helvetica', size=12)
        collectButton["fg"] = "#000000"
        collectButton["justify"] = "center"
        collectButton["text"] = "Collect\nMenu"
        collectButton.grid(row = 2, sticky='nw', column = 2, columnspan=2, rowspan=2)
        collectButton["command"] = self.loadCollectMenu

        exportButton=tk.Button(self.root, height=5, width=15)
        exportButton["bg"] = ControlPanelGUI.highlightColor
        exportButton["font"] = tkFont.Font(family='Helvetica', size=12)
        exportButton["fg"] = "#000000"
        exportButton["justify"] = "center"
        exportButton["text"] = "Export to\nUSB"
        exportButton.grid(row = 2, sticky='nw', padx=10 , column = 4, columnspan=2, rowspan=2)
        exportButton["command"] = self.saveToUSB


    def configureScreen(self):
        """
        Populate the grid with the CALIBRATION menu
        """

        self.root.title("CONFIGURE MENU")

        # Place LOGO
        logo = Image.open(self.DIR + "/icons/logo.png")
        logo = logo.resize((140, 50), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(logo)
        logoLabel = Label(self.root, image=logo)
        logoLabel.image = logo
        logoLabel.grid(row = 0, column = 0, padx=10, ipady=10, sticky='nw', columnspan=2)

        # Place HOME Button
        home = Image.open(self.DIR + "/icons/home.png")
        home = home.resize((50, 50), Image.ANTIALIAS)
        home = ImageTk.PhotoImage(home)       
        homeButton=tk.Button(self.root, bd=0, image=home)
        homeButton.image = home
        homeButton.grid(row = 0, column = 3, padx=10, ipady=5, sticky='ne', columnspan=2,  rowspan=1)
        homeButton["command"] = self.loadHomeMenu
        
        nameLabel=tk.Label(self.root)
        nameLabel["font"] = tkFont.Font(family='Helvetica', weight="bold", size=14)
        nameLabel["fg"] = "#000000"
        nameLabel["justify"] = "center"
        nameLabel["text"] = "Configuration Menu"
        nameLabel.grid(row = 1, column = 0, padx=10, columnspan = 7, sticky='ew')

        obLabel=tk.Label(self.root)
        obLabel["font"] = tkFont.Font(family='Helvetica', size=10)
        obLabel["fg"] = "#000000"
        obLabel["text"] = "Orientation Board"
        obLabel.grid(row = 2, column = 1, sticky='s')
        ControlPanelGUI.createEnButton(self, self.root, 3, 1, 'OB', 'EN')
        ControlPanelGUI.createZeroButton(self, self.root, 4, 1, 'OB', 'ZERO')

        scalLabel=tk.Label(self.root)
        scalLabel["font"] = tkFont.Font(family='Helvetica', size=10)
        scalLabel["text"] = "Scale"
        scalLabel.grid(row = 2, column = 2, sticky='s')
        ControlPanelGUI.createEnButton(self, self.root, 3, 2, 'SCAL', 'EN')
        ControlPanelGUI.createZeroButton(self, self.root, 4, 2, 'SCAL', 'ZERO')

        fsrLabel=tk.Label(self.root)
        fsrLabel["font"] = tkFont.Font(family='Helvetica', size=10)
        #nameLabel["bg"] = highlightColor
        fsrLabel["fg"] = "#000000"
        fsrLabel["text"] = "Force Sensors"
        fsrLabel.grid(row = 2, column = 3, sticky='s')
        ControlPanelGUI.createEnButton(self, self.root, 3, 3, 'FSR', 'EN')
        ControlPanelGUI.createZeroButton(self, self.root, 4, 3, 'FSR', 'ZERO')

        imuLabel=tk.Label(self.root)
        imuLabel["font"] = tkFont.Font(family='Helvetica', size=10)
        #nameLabel["bg"] = highlightColor
        imuLabel["fg"] = "#000000"
        imuLabel["text"] = "IMU Sensors"
        imuLabel.grid(row = 2, column = 4, sticky='s')
        ControlPanelGUI.createEnButton(self, self.root, 3, 4, 'IMU', 'EN')
        ControlPanelGUI.createZeroButton(self, self.root, 4, 4, 'IMU', 'ZERO')


    def collectScreen(self):
        """
        Populate the grid with the POLLING menue
        """

        self.root.title("COLLECT DATA MENU")

        # Place LOGO
        logo = Image.open(self.DIR + "/icons/logo.png")
        logo = logo.resize((140, 50), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(logo)
        logoLabel = Label(self.root, image=logo)
        logoLabel.image = logo
        logoLabel.grid(row = 0, column = 0, padx=10, ipady=10, sticky='nw', columnspan=2)

        # Place HOME Button
        home = Image.open(self.DIR + "/icons/home.png")
        home = home.resize((50, 50), Image.ANTIALIAS)
        home = ImageTk.PhotoImage(home)       
        homeButton=tk.Button(self.root, bd=0, image=home)
        homeButton.image = home
        homeButton.grid(row = 0, column = 3, padx=10, ipady=5, sticky='ne', columnspan=2,  rowspan=1)
        homeButton["command"] = self.loadHomeMenu

        nameLabel=tk.Label(self.root)
        nameLabel["font"] = tkFont.Font(family='Helvetica', weight="bold", size=14)
        nameLabel["fg"] = "#000000"
        nameLabel["justify"] = "center"
        nameLabel["text"] = "Collection Menu"
        nameLabel.grid(row = 1, column = 0, columnspan = 6, sticky='ew')

        statusLabel=tk.Label(self.root)
        statusLabel["font"] = tkFont.Font(family='Helvetica', size=10)
        statusLabel["fg"] = "#000000"
        statusLabel["justify"] = "center"
        statusLabel["text"] = "Status: PAUSED"
        statusLabel.grid(row = 2, column = 0, columnspan = 6, sticky='n')

        # START TESTING BUTTON
        start = Image.open(self.DIR + "/icons/play.png")
        start = start.resize((75, 75), Image.ANTIALIAS)
        start = ImageTk.PhotoImage(start)       
        startButton=tk.Button(self.root, bd=0, bg=ControlPanelGUI.highlightColor, image=start)
        startButton.image = start
        startButton.grid(row = 3, column = 0, pady=50, ipady=25, columnspan=2,  rowspan=2, sticky='ew')
        startButton["command"] = lambda: self.startEvent(statusLabel)

        # STOP TESTING BUTTON
        stop = Image.open(self.DIR + "/icons/pause.png")
        stop = stop.resize((75, 75), Image.ANTIALIAS)
        stop = ImageTk.PhotoImage(stop)       
        stopButton=tk.Button(self.root, bd=0, bg=ControlPanelGUI.highlightColor, image=stop)
        stopButton.image = stop
        stopButton.grid(row = 3, column = 2, pady=50, ipady=25, columnspan=3,  rowspan=2, sticky='ew')
        stopButton["command"] = lambda: self.stopEvent(statusLabel)


    def loadConfigureMenu(self):
        """
        BUTTON METHOD - Switch screens to Config Menue
        """
        #print("CONFIGURE MENU")
        self.clearGrid()
        self.configureScreen()


    def loadCollectMenu(self):
        """
        BUTTON METHOD - Switch screens to Collect Menue
        """
        #print("DATA COLLECTION MENU")
        self.clearGrid()
        self.collectScreen()


    def loadHomeMenu(self):
        """
        BUTTON METHOD - Switch screens to Home Menue
        """
        #print("HOME MENU")
        self.collect_en = False
        self.mcuComms.send_cmd("SYS", "GLBL", "EN", "0\n")
        self.clearGrid()
        self.bootScreen()


    def saveToUSB(self):
        """
        BUTTON METHOD - Call on MCU_Comms to save test to USB Stick
        """
        #print("SAVING DATA TO USB")
        self.mcuComms.saveUSB()
    

    def startEvent(self, status):
        """
        BUTTON METHOD - Begin data polling

        Args:
            status (boolean): Is data polling(?) flag
        """
        #print("START DATA COLLECTION")
        if not self.collect_en:
            self.collect_en = True
            self.data_thread = threading.Thread(target=self.mcuComms.poll_data, args=(lambda : self.collect_en, ))
            #self.status_thread = threading.Thread(target=self.mcuComms.poll_status, args=(lambda : self.collect_en, ))
            self.data_thread.start()
            #self.status_thread.start()
            self.mcuComms.send_cmd("SYS", "GLBL", "EN", "1\n")
            status["text"] = "Status: LOGGING"


    def stopEvent(self, status):
        """
        BUTTON METHOD - Stop data polling

        Args:
            status (boolean): Is data polling(?) flag
        """
        #print("STOP DATA COLLECTION")
        if self.collect_en:
            self.mcuComms.send_cmd("SYS", "GLBL", "EN", "0\n")
            self.collect_en = False
            #self.data_thread.join()
            #self.status_thread.join()
            status["text"] = "Status: PAUSED"
        

    def isSensorEnabled(self, sensor):
        """
        Get sensor enable(?) flag

        Args:
            sensor (String): Sensor's Name

        Returns:
            [boolean]: Flag as to whether or not the sensor in question is enabled
        """
        if (sensor == "OB"):
            return self.obEnFlag
        if (sensor == "SCAL"):
            return self.scaleEnFlag
        if (sensor == "FSR"):
            return self.fsrEnFlag
        if (sensor == "IMU"):
            return self.imuEnFlag


    def enSensor(self, sensor, type, button):
        """
        Enable the sensor

        Args:
            sensor (String): The string name of the sensor
            type (String): The string type of the sensor
            button (String): The button the sensor correlates to
        """
        # Toggle the enable flag and set the locations.
        locations = []
        if sensor == "OB":
            self.obEnFlag = not self.isSensorEnabled(sensor)
            locations.append("H")
            locations.append("B")
        elif sensor == "SCAL":
            self.scaleEnFlag = not self.isSensorEnabled(sensor)
            locations.append("CH")
        elif sensor == "FSR":
            self.fsrEnFlag = not self.isSensorEnabled(sensor)
            locations.append("LR")
            locations.append("RR")
            locations.append("LH")
            locations.append("RH")
            locations.append("LF")
            locations.append("RF")
            locations.append("LK")
            locations.append("RK")
        elif sensor == "IMU":
            self.imuEnFlag = not self.isSensorEnabled(sensor)
            locations.append("LL")
            locations.append("RL")

        if (self.isSensorEnabled(sensor)):
            # Enable sensor.
            button["bg"] = self.highlightColor
            button["text"] = "DISABLE"
            for loc in locations:
                self.mcuComms.send_cmd(sensor, loc, type, "1")
        else:
            # Disable sensor.
            button["bg"] = self.grayColor
            button["text"] = "ENABLE"
            for loc in locations:
                self.mcuComms.send_cmd(sensor, loc, type, "0")


    def zeroSensor(self, sensor, type):
        """
        Zero the sensor

        Args:
            sensor (String): The string name of the sensor
            type (String): The string type of the sensor

        """

        #print("ZEROING: " + sensor + ", " + type)
        if (self.isSensorEnabled(sensor)):
            locations = []
            if sensor == "OB":
                locations.append("H")
                locations.append("B")
            elif sensor == "SCAL":
                locations.append("CH")
            elif sensor == "FSR":
                locations.append("LR")
                locations.append("RR")
                locations.append("LH")
                locations.append("RH")
                locations.append("LF")
                locations.append("RF")
                locations.append("LK")
                locations.append("RK")
            elif sensor == "IMU":
                locations.append("LL")
                locations.append("RL")
            
            for loc in locations:
                if sensor == "OB" or sensor == "IMU":
                    self.mcuComms.send_cmd(sensor, loc, type, "1>1")
                else:
                    self.mcuComms.send_cmd(sensor, loc, type, "")
        

if __name__ == "__main__":
    """
    Main Method
    """
    root = tk.Tk()
    gui_thread = ControlPanelGUI(root)
    root.mainloop()
