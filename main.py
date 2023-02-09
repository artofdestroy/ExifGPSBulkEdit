import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMsgBox
import csv

class App:
    def __init__(self, root):
        #setting title
        self.root = root
        self.root.title("Bulk GPS EXIF writer")
        #setting window size
        width=480
        height=320
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        self.pic_dir_lb=tk.Label(self.root)
        ft = tkFont.Font(family='Times',size=10)
        self.pic_dir_lb["font"] = ft
        self.pic_dir_lb["fg"] = "#333333"
        self.pic_dir_lb["justify"] = "center"
        self.pic_dir_lb["text"] = "Picture folder"
        self.pic_dir_lb.place(x=20,y=20,width=90,height=30)

        self.csv_path_lb=tk.Label(self.root)
        ft = tkFont.Font(family='Times',size=10)
        self.csv_path_lb["font"] = ft
        self.csv_path_lb["fg"] = "#333333"
        self.csv_path_lb["justify"] = "center"
        self.csv_path_lb["text"] = "CSV File"
        self.csv_path_lb.place(x=20,y=60,width=90,height=30)

        self.pic_dir_but=tk.Button(self.root)
        self.pic_dir_but["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=10)
        self.pic_dir_but["font"] = ft
        self.pic_dir_but["fg"] = "#000000"
        self.pic_dir_but["justify"] = "center"
        self.pic_dir_but["text"] = "SELECT"
        self.pic_dir_but.place(x=390,y=20,width=70,height=30)
        self.pic_dir_but["command"] = self.pic_dir_but_clicked

        self.csv_path_but=tk.Button(self.root)
        self.csv_path_but["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=10)
        self.csv_path_but["font"] = ft
        self.csv_path_but["fg"] = "#000000"
        self.csv_path_but["justify"] = "center"
        self.csv_path_but["text"] = "SELECT"
        self.csv_path_but.place(x=390,y=60,width=70,height=30)
        self.csv_path_but["command"] = self.csv_path_but_clicked

        self.start_but=tk.Button(self.root)
        self.start_but["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=10)
        self.start_but["font"] = ft
        self.start_but["fg"] = "#000000"
        self.start_but["justify"] = "center"
        self.start_but["text"] = "START"
        self.start_but.place(x=200,y=120,width=80,height=30)
        self.start_but["command"] = self.start_but_clicked

        self.csv_path_tb=tk.Entry(self.root)
        self.csv_path_tb["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.csv_path_tb["font"] = ft
        self.csv_path_tb["fg"] = "#333333"
        self.csv_path_tb["justify"] = "left"
        self.csv_path_tb.place(x=140,y=60,width=240,height=30)

        self.pic_dir_tb=tk.Entry(master=self.root)
        self.pic_dir_tb["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.pic_dir_tb["font"] = ft
        self.pic_dir_tb["fg"] = "#333333"
        self.pic_dir_tb["justify"] = "left"
        self.pic_dir_tb.place(x=140,y=20,width=240,height=30)

        file_tree_col = ("file_name", "lat", "long", "alt")
        self.file_list_tree = ttk.Treeview(master=self.root, columns=file_tree_col, show="headings")
        self.file_list_tree.heading("file_name", text="File name")
        self.file_list_tree.heading("lat", text="Latitude")
        self.file_list_tree.column("lat", width=70)
        self.file_list_tree.heading("long", text="Longitude")
        self.file_list_tree.column("long", width=70)
        self.file_list_tree.heading("alt", text="Altitude")
        self.file_list_tree.column("alt", width=70)
        self.file_list_tree.place(x=20,y=180,width=440,height=120)

    def pic_dir_but_clicked(self):
        pic_dir_path = tkFileDialog.askdirectory()
        if pic_dir_path != "":
            print(f"select dir:{pic_dir_path}")
            self.pic_dir_tb.delete(0, "end")
            self.pic_dir_tb.insert(0, pic_dir_path)


    def csv_path_but_clicked(self):
        csv_path_tuple = tkFileDialog.askopenfilenames()
        if csv_path_tuple != "":
            csv_path = csv_path_tuple[0]
            print(f"select csv:{csv_path}")
            self.csv_path_tb.delete(0, "end")
            self.csv_path_tb.insert(0, csv_path)
        else:
            print("Cancel select file")


    def start_but_clicked(self):
        print("start_but_clicked")
        csv_path = self.csv_path_tb.get()
        pic_dir_path = self.pic_dir_tb.get()
        print(csv_path)
        print(pic_dir_path)
        if csv_path != "" and pic_dir_path != "":
            print("All file present")
            with open(csv_path, newline='') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")
                for row in csv_reader:
                    print(row)
                    self.file_list_tree.insert("", tk.END, values=row)
        else:
            tkMsgBox.showerror(title="Please select file", message="Please select picture folder and csv file")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
