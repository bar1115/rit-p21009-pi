import tkinter as tk
import tkinter.font as tkFont

class UserInterface:
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_293=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_293["font"] = ft
        GLabel_293["fg"] = "#333333"
        GLabel_293["justify"] = "center"
        GLabel_293["text"] = "Footer"
        GLabel_293.place(x=0,y=410,width=600,height=86)

        GLabel_476=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_476["font"] = ft
        GLabel_476["fg"] = "#333333"
        GLabel_476["justify"] = "center"
        GLabel_476["text"] = "Header"
        GLabel_476.place(x=0,y=60,width=600,height=59)

        GButton_442=tk.Button(root)
        GButton_442["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_442["font"] = ft
        GButton_442["fg"] = "#000000"
        GButton_442["justify"] = "center"
        GButton_442["text"] = "Start"
        GButton_442.place(x=10,y=450,width=92,height=43)
        GButton_442["command"] = self.GButton_442_command

        GLabel_634=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_634["font"] = ft
        GLabel_634["fg"] = "#333333"
        GLabel_634["justify"] = "center"
        GLabel_634["text"] = "Body of the Display"
        GLabel_634.place(x=250,y=210,width=150,height=25)

        GButton_215=tk.Button(root)
        GButton_215["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_215["font"] = ft
        GButton_215["fg"] = "#000000"
        GButton_215["justify"] = "center"
        GButton_215["text"] = "Stop"
        GButton_215.place(x=130,y=450,width=92,height=42)
        GButton_215["command"] = self.GButton_215_command

        GButton_844=tk.Button(root)
        GButton_844["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_844["font"] = ft
        GButton_844["fg"] = "#000000"
        GButton_844["justify"] = "center"
        GButton_844["text"] = "Save"
        GButton_844.place(x=360,y=450,width=92,height=44)
        GButton_844["command"] = self.GButton_844_command

        GButton_0=tk.Button(root)
        GButton_0["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_0["font"] = ft
        GButton_0["fg"] = "#000000"
        GButton_0["justify"] = "center"
        GButton_0["text"] = "Send"
        GButton_0.place(x=480,y=450,width=92,height=44)
        GButton_0["command"] = self.GButton_0_command

        GMessage_430=tk.Message(root)
        ft = tkFont.Font(family='Times',size=10)
        GMessage_430["font"] = ft
        GMessage_430["fg"] = "#333333"
        GMessage_430["justify"] = "center"
        GMessage_430["text"] = "Livability Lab Logo"
        GMessage_430.place(x=0,y=20,width=80,height=25)

        GButton_461=tk.Button(root)
        GButton_461["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_461["font"] = ft
        GButton_461["fg"] = "#000000"
        GButton_461["justify"] = "center"
        GButton_461["text"] = "Data"
        GButton_461.place(x=110,y=10,width=82,height=30)
        GButton_461["command"] = self.GButton_461_command

        GButton_771=tk.Button(root)
        GButton_771["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_771["font"] = ft
        GButton_771["fg"] = "#000000"
        GButton_771["justify"] = "center"
        GButton_771["text"] = "Report"
        GButton_771.place(x=190,y=10,width=75,height=30)
        GButton_771["command"] = self.GButton_771_command

    def GButton_442_command(self):
        print("start collecting data")


    def GButton_215_command(self):
        print("stop collecting data")


    def GButton_844_command(self):
        print("save data")


    def GButton_0_command(self):
        print("send data")


    def GButton_461_command(self):
        print("This activates the data tab")


    def GButton_771_command(self):
        print("This activates the report tab")

if __name__ == "__main__":
    root = tk.Tk()
    app = UserInterface(root)
    root.mainloop()
