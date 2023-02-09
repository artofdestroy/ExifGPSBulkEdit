import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size
        width=480
        height=320
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_868=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_868["font"] = ft
        GLabel_868["fg"] = "#333333"
        GLabel_868["justify"] = "center"
        GLabel_868["text"] = "Picture folder"
        GLabel_868.place(x=20,y=20,width=90,height=30)

        GLabel_647=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_647["font"] = ft
        GLabel_647["fg"] = "#333333"
        GLabel_647["justify"] = "center"
        GLabel_647["text"] = "CSV File"
        GLabel_647.place(x=20,y=60,width=90,height=30)

        GButton_55=tk.Button(root)
        GButton_55["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=10)
        GButton_55["font"] = ft
        GButton_55["fg"] = "#000000"
        GButton_55["justify"] = "center"
        GButton_55["text"] = "SELECT"
        GButton_55.place(x=390,y=20,width=70,height=30)
        GButton_55["command"] = self.GButton_55_command

        GButton_829=tk.Button(root)
        GButton_829["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=10)
        GButton_829["font"] = ft
        GButton_829["fg"] = "#000000"
        GButton_829["justify"] = "center"
        GButton_829["text"] = "SELECT"
        GButton_829.place(x=390,y=60,width=70,height=30)
        GButton_829["command"] = self.GButton_829_command

        GButton_383=tk.Button(root)
        GButton_383["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=10)
        GButton_383["font"] = ft
        GButton_383["fg"] = "#000000"
        GButton_383["justify"] = "center"
        GButton_383["text"] = "START"
        GButton_383.place(x=200,y=120,width=80,height=30)
        GButton_383["command"] = self.GButton_383_command

        GLineEdit_532=tk.Entry(root)
        GLineEdit_532["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_532["font"] = ft
        GLineEdit_532["fg"] = "#333333"
        GLineEdit_532["justify"] = "center"
        GLineEdit_532["text"] = "CSV_PATH_TB"
        GLineEdit_532.place(x=140,y=60,width=240,height=30)

        GLineEdit_486=tk.Entry(root)
        GLineEdit_486["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_486["font"] = ft
        GLineEdit_486["fg"] = "#333333"
        GLineEdit_486["justify"] = "center"
        GLineEdit_486["text"] = "PIC_DIR_TB"
        GLineEdit_486.place(x=140,y=20,width=240,height=30)

        GLineEdit_897=tk.Entry(root)
        GLineEdit_897["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_897["font"] = ft
        GLineEdit_897["fg"] = "#333333"
        GLineEdit_897["justify"] = "left"
        GLineEdit_897["text"] = "ERR_LIST"
        GLineEdit_897.place(x=20,y=180,width=440,height=120)

    def GButton_55_command(self):
        print("command")


    def GButton_829_command(self):
        print("command")


    def GButton_383_command(self):
        print("command")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
