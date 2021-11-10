import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from PIL import Image, ImageTk

class UserInterface:

    def __init__(self, root):
        """
        Initialize the Buttons and Label graphics

        Args:
            root (Tk): The tkinter object necessary to estable layout
        """

        # Setting - Title
        root.title("undefined")

        # Setting - Window Size
        width=480
        height=320
        highlightColor = "#85d3e9"
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        # TASK BAR BAND
        bottomBar=tk.Label(root)
        bottomBar["bg"] = highlightColor
        bottomBar.pack( ipady=12, side='bottom', fill='x' )

        # START TESTING BUTTON
        start = Image.open("icons\play.png")
        start = start.resize((25, 25), Image.ANTIALIAS)
        start = ImageTk.PhotoImage(start)       
        startButton=tk.Button(root, bg=highlightColor, bd=0, image=start)
        startButton.image = start
        startButton.place(x=10,y=280,width=50,height=40)
        startButton["command"] = self.startEvent

        # STOP TESTING BUTTON
        stop = Image.open("icons\pause.png")
        stop = stop.resize((25, 25), Image.ANTIALIAS)
        stop = ImageTk.PhotoImage(stop)       
        stopButton=tk.Button(root, bg=highlightColor, bd=0, image=stop)
        stopButton.image = stop
        stopButton.place(x=100,y=280,width=50,height=40)
        stopButton["command"] = self.stopEvent

        # SAVE DATA TO USB
        save = Image.open("icons\save.png")
        save = save.resize((25, 25), Image.ANTIALIAS)
        save = ImageTk.PhotoImage(save)
        saveButton=tk.Button(root, bg=highlightColor, bd=0, image=save)
        saveButton.image = save
        saveButton.place(x=330,y=280,width=50,height=40)
        saveButton["command"] = self.saveButton_command

        # 
        send = Image.open("icons\send.png")
        send = send.resize((25, 25), Image.ANTIALIAS)
        send = ImageTk.PhotoImage(send)
        sendButton=tk.Button(root, bg=highlightColor, bd=0, image=send)
        sendButton.image = send
        sendButton.place(x=420,y=280,width=50,height=40)
        sendButton["command"] = self.sendEvent

        dataButton=tk.Button(root)
        dataButton["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        dataButton["font"] = ft
        dataButton["fg"] = "#000000"
        dataButton["justify"] = "center"
        dataButton["text"] = "Data"
        dataButton.place(x=140,y=10,width=82,height=30)
        dataButton["command"] = self.dataEvent

        reportButton=tk.Button(root)
        reportButton["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        reportButton["font"] = ft
        reportButton["fg"] = "#000000"
        reportButton["justify"] = "center"
        reportButton["text"] = "Report"
        reportButton.place(x=250,y=10,width=75,height=30)
        reportButton["command"] = self.reportEvent

        logo = Image.open("icons/logo.png")
        logo = logo.resize((115, 35), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(logo)
        logoLabel = Label(root, image=logo)
        logoLabel.image = logo
        #logoLabel.pack()
        logoLabel.place(x = 5 , y = 5)
        

    def startEvent(self):
        print("start collecting data")


    def stopEvent(self):
        print("stop collecting data")


    def saveButton_command(self):
        print("save data")


    def sendEvent(self):
        print("send data")


    def dataEvent(self):
        print("This activates the data tab")


    def reportEvent(self):
        print("This activates the report tab")

if __name__ == "__main__":
    root = tk.Tk()
    app = UserInterface(root)
    root.mainloop()