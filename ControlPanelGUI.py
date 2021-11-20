#########################################################################################
#                                                                                       #
#   File    : ControlPanelGUI.py                                                        #
#   Author  : Thomas Sosa (ts5630@rit.edu) & Rebecca Reich (bar1115@rit.edu)            #
#   Created : ‎October ‎7, ‎2021                                   #    
#                                                                                       #
#   Description:                                                                        #
#     The Control Panel GUI, which creates the labels, buttons and button events        #   
#     graphics on the systems touch-logoLabel controller                                #
#                                                                                       #
#########################################################################################

import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
import threading
from PIL import Image, ImageTk

from MCU_Comms import MCU_Comms


class ControlPanelGUI(threading.Thread):

    WIDTH       = 480
    HEIGHT      = 320
    GRID_DIM    = 6
    
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
        self.poll_data_en = False
        self.poll_status_en = False
            
        self.start()
    

    def run(self):
        self.bootScreen()


    def clearGrid(self):
        # Clear all elements in the window
        for widget in self.root.winfo_children():
            widget.destroy()


    def createCalButton(self, root, r, c, sensor, type):
        calButton=tk.Button(root, width=20)
        calButton["bg"] = ControlPanelGUI.highlightColor
        calButton["font"] = tkFont.Font(family='Helvetica', size=12)
        calButton["text"] = "CAL"
        calButton.grid(row = r, column = c, sticky='n', padx=10, ipady=7)
        calButton["command"] = lambda: self.calSensor(sensor, type)


    def createZeroButton(self, root, r, c, sensor, type):
        scalLabel=tk.Button(root, width=20)
        scalLabel["bg"] = ControlPanelGUI.highlightColor
        scalLabel["font"] = tkFont.Font(family='Helvetica', size=12)
        scalLabel["text"] = "ZERO"
        scalLabel.grid(row = r, column = c, sticky='n', padx=10, ipady=10)
        scalLabel["command"] = lambda: self.zeroSensor(sensor, type)


    def bootScreen( self ):

        self.root.title("BOOT MENU")

        logo = Image.open("icons/logo.png")
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

        calMenuButton=tk.Button(self.root, height=5, width=15)
        calMenuButton["bg"] = ControlPanelGUI.highlightColor
        calMenuButton["font"] = tkFont.Font(family='Helvetica', size=12)
        calMenuButton["fg"] = "#000000"
        calMenuButton["justify"] = "center"
        calMenuButton["text"] = "Calibrate\nMenu"
        calMenuButton.grid(row = 2, sticky='n', padx=10, column = 0, columnspan=2, rowspan=2)
        calMenuButton["command"] = self.loadCalibrateMenu

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


    def calibrateScreen(self):

        self.root.title("CALIBRATE MENU")

        # Place LOGO
        logo = Image.open("icons/logo.png")
        logo = logo.resize((140, 50), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(logo)
        logoLabel = Label(self.root, image=logo)
        logoLabel.image = logo
        logoLabel.grid(row = 0, column = 0, padx=10, ipady=10, sticky='nw', columnspan=2)

        # Place HOME Button
        home = Image.open("icons/home.png")
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
        nameLabel["text"] = "Calibration Menu"
        nameLabel.grid(row = 1, column = 0, padx=10, columnspan = 7, sticky='ew')

        obLabel=tk.Label(self.root)
        obLabel["font"] = tkFont.Font(family='Helvetica', size=10)
        obLabel["fg"] = "#000000"
        obLabel["text"] = "Orientation Board"
        obLabel.grid(row = 2, column = 1, sticky='s')
        ControlPanelGUI.createCalButton(self, self.root, 3, 1, 'OB', 'CAL')
        ControlPanelGUI.createZeroButton(self, self.root, 4, 1, 'OB', 'ZERO')

        scalLabel=tk.Label(self.root)
        scalLabel["font"] = tkFont.Font(family='Helvetica', size=10)
        scalLabel["text"] = "Scale"
        scalLabel.grid(row = 2, column = 2, sticky='s')
        ControlPanelGUI.createCalButton(self, self.root, 3, 2, 'SCAL', 'CAL')
        ControlPanelGUI.createZeroButton(self, self.root, 4, 2, 'SCAL', 'ZERO')

        fsrLabel=tk.Label(self.root)
        fsrLabel["font"] = tkFont.Font(family='Helvetica', size=10)
        #nameLabel["bg"] = highlightColor
        fsrLabel["fg"] = "#000000"
        fsrLabel["text"] = "Force Sensors"
        fsrLabel.grid(row = 2, column = 3, sticky='s')
        ControlPanelGUI.createCalButton(self, self.root, 3, 3, 'FSR', 'CAL')
        ControlPanelGUI.createZeroButton(self, self.root, 4, 3, 'FSR', 'ZERO')


    def collectScreen(self):

        self.root.title("COLLECT DATA MENU")

        # Place LOGO
        logo = Image.open("icons/logo.png")
        logo = logo.resize((140, 50), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(logo)
        logoLabel = Label(self.root, image=logo)
        logoLabel.image = logo
        logoLabel.grid(row = 0, column = 0, padx=10, ipady=10, sticky='nw', columnspan=2)

        # Place HOME Button
        home = Image.open("icons/home.png")
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
        nameLabel["text"] = "Test Menu"
        nameLabel.grid(row = 1, column = 0, columnspan = 6, sticky='ew')

        nameLabel=tk.Label(self.root)
        nameLabel["font"] = tkFont.Font(family='Helvetica', size=10)
        nameLabel["fg"] = "#000000"
        nameLabel["justify"] = "center"
        nameLabel["text"] = "Status: LOGGING"
        nameLabel.grid(row = 2, column = 0, columnspan = 6, sticky='n')

        # START TESTING BUTTON
        start = Image.open("icons\play.png")
        start = start.resize((75, 75), Image.ANTIALIAS)
        start = ImageTk.PhotoImage(start)       
        startButton=tk.Button(self.root, bd=0, bg=ControlPanelGUI.highlightColor, image=start)
        startButton.image = start
        startButton.grid(row = 3, column = 0, ipady=25, columnspan=2,  rowspan=2, sticky='ew')
        startButton["command"] = self.startEvent

        # STOP TESTING BUTTON
        stop = Image.open("icons\pause.png")
        stop = stop.resize((75, 75), Image.ANTIALIAS)
        stop = ImageTk.PhotoImage(stop)       
        stopButton=tk.Button(self.root, bd=0, bg=ControlPanelGUI.highlightColor, image=stop)
        stopButton.image = stop
        stopButton.grid(row = 3, column = 2, ipady=25, columnspan=3,  rowspan=2, sticky='ew')
        stopButton["command"] = self.stopEvent


    def loadCalibrateMenu(self):
        print("GO TO CALIBRATE MENU")
        self.clearGrid()
        self.calibrateScreen()


    def loadCollectMenu(self):
        print("GO TO DATA COLLECTION MENU")
        self.clearGrid()
        self.collectScreen()


    def loadHomeMenu(self):
        print("GO TO HOME MENU")
        self.poll_data_en = False
        self.poll_status_en = False
        self.clearGrid()
        self.bootScreen()


    def saveToUSB(self):
        print("Save Data to USB")


    def startEvent(self):
        if not self.poll_status_en:
            print("Start collecting data")
            self.poll_status_en = True
            self.status_thread = threading.Thread(target=self.mcuComms.poll_data, args=(lambda : self.poll_status_en, ))
            self.status_thread.start()
        else:
            print("Already collecting data!")


    def stopEvent(self):
        print("Stop collecting data")
        self.poll_status_en = False
        self.status_thread.join()


    def calSensor(self, sensor, type):
        print("calibrate sensor: " + sensor + ", " + type)


    def zeroSensor(self, sensor, type):
        print("zero sensor: " + sensor + ", " + type)
        

if __name__ == "__main__":
    root = tk.Tk()
    gui_thread = ControlPanelGUI(root)
    root.mainloop()