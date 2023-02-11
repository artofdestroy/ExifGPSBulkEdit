import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMsgBox
import csv
import os
from threading import Thread
from dataclasses import dataclass
import piexif

@dataclass
class ImageDetailDec:
    file_path : str
    lat_dec : float
    long_dec : float
    altitude : float

class App:
    def __init__(self, root):
        #setting title
        self.root = root
        self.root.title("Bulk GPS EXIF writer")
        #setting window size
        width=800
        height=600
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        # Picture directory
        self.pic_dir_lb=tk.Label(self.root)
        ft = tkFont.Font(family='Times',size=10)
        self.pic_dir_lb["font"] = ft
        self.pic_dir_lb["fg"] = "#333333"
        self.pic_dir_lb["justify"] = "center"
        self.pic_dir_lb["text"] = "Picture folder"
        self.pic_dir_lb.place(x=20,y=20,width=90,height=30)

        self.pic_dir_tb=tk.Entry(master=self.root)
        self.pic_dir_tb["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.pic_dir_tb["font"] = ft
        self.pic_dir_tb["fg"] = "#333333"
        self.pic_dir_tb["justify"] = "left"
        self.pic_dir_tb.place(x=140,y=20,width=550,height=30)

        self.pic_dir_but=tk.Button(self.root)
        self.pic_dir_but["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=10)
        self.pic_dir_but["font"] = ft
        self.pic_dir_but["fg"] = "#000000"
        self.pic_dir_but["justify"] = "center"
        self.pic_dir_but["text"] = "SELECT"
        self.pic_dir_but.place(x=700,y=20,width=70,height=30)
        self.pic_dir_but["command"] = self.pic_dir_but_clicked


        # CSV Path
        self.csv_path_lb=tk.Label(self.root)
        ft = tkFont.Font(family='Times',size=10)
        self.csv_path_lb["font"] = ft
        self.csv_path_lb["fg"] = "#333333"
        self.csv_path_lb["justify"] = "center"
        self.csv_path_lb["text"] = "CSV File"
        self.csv_path_lb.place(x=20,y=60,width=90,height=30)

        self.csv_path_tb=tk.Entry(self.root)
        self.csv_path_tb["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.csv_path_tb["font"] = ft
        self.csv_path_tb["fg"] = "#333333"
        self.csv_path_tb["justify"] = "left"
        self.csv_path_tb.place(x=140,y=60,width=550,height=30)

        self.csv_path_but=tk.Button(self.root)
        self.csv_path_but["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=10)
        self.csv_path_but["font"] = ft
        self.csv_path_but["fg"] = "#000000"
        self.csv_path_but["justify"] = "center"
        self.csv_path_but["text"] = "SELECT"
        self.csv_path_but.place(x=700,y=60,width=70,height=30)
        self.csv_path_but["command"] = self.csv_path_but_clicked


        # Start button
        self.start_but=tk.Button(self.root)
        self.start_but["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=10)
        self.start_but["font"] = ft
        self.start_but["fg"] = "#000000"
        self.start_but["justify"] = "center"
        self.start_but["text"] = "START"
        self.start_but.place(x=360,y=550,width=80,height=30)
        self.start_but["command"] = self.start_but_clicked


        # File table
        file_tree_col = ("img_name", "lat_dec", "long_dec", "alt")
        self.file_list_tree = ttk.Treeview(master=self.root, columns=file_tree_col, show="headings", selectmode='browse')
        self.file_list_tree.heading("img_name", text="Image name")
        self.file_list_tree.heading("lat_dec", text="Latitude")
        self.file_list_tree.column("lat_dec", width=70)
        self.file_list_tree.heading("long_dec", text="Longitude")
        self.file_list_tree.column("long_dec", width=70)
        self.file_list_tree.heading("alt", text="Altitude")
        self.file_list_tree.column("alt", width=70)
        self.file_list_tree.place(x=20,y=120,width=740,height=390)

        file_list_tree_bar = tk.Scrollbar(master=self.root, orient="vertical", command=self.file_list_tree.yview)
        file_list_tree_bar.place(x=760, y=120, height=400, width=20)
        self.file_list_tree.configure(yscrollcommand=file_list_tree_bar.set)


        # Status
        self.sts_lb=tk.Label(self.root)
        ft = tkFont.Font(family='Times',size=10)
        self.sts_lb["font"] = ft
        self.sts_lb["fg"] = "#333333"
        self.sts_lb["justify"] = "left"
        self.sts_lb["text"] = ""
        self.sts_lb.place(x=20,y=510,width=400,height=30)


        # Other object
        self.convert_thr = None

    def pic_dir_but_clicked(self):
        pic_dir_path = tkFileDialog.askdirectory()
        if pic_dir_path != "":
            print(f"select dir:{pic_dir_path}")
            self.pic_dir_tb.delete(0, "end")
            self.pic_dir_tb.insert(0, pic_dir_path)
            self.pic_dir_tb.focus()
            self.pic_dir_tb.icursor("end")


    def csv_path_but_clicked(self):
        csv_path_tuple = tkFileDialog.askopenfilenames(filetypes=[("CSV File", ".csv")])
        if csv_path_tuple != "":
            csv_path = csv_path_tuple[0]
            print(f"select csv:{csv_path}")
            self.csv_path_tb.delete(0, "end")
            self.csv_path_tb.insert(0, csv_path)
            self.csv_path_tb.focus()
            self.csv_path_tb.icursor("end")

            detail_list = self.load_raw_csv(csv_path)
            self.gen_file_list(detail_list)
        else:
            print("Cancel select file")

    def start_but_clicked(self):
        print("start_but_clicked")
        csv_path = self.csv_path_tb.get()
        pic_dir_path = self.pic_dir_tb.get()
        if csv_path != "" and pic_dir_path != "":
            self.convert_thr = Thread(target=self.convert_job)
            self.convert_thr.start()
        else:
            tkMsgBox.showerror(title="Please select file", message="Please select picture folder and csv file")

    # Disable all editable widget
    def disable_all_but_field(self):
        self.pic_dir_but["state"] = "disabled"
        self.pic_dir_tb["state"] = "disabled"
        self.csv_path_but["state"] = "disabled"
        self.csv_path_tb["state"] = "disabled"
        self.start_but["state"] = "disabled"

    # Enable all editable widget
    def enable_all_but_field(self):
        self.pic_dir_but["state"] = "normal"
        self.pic_dir_tb["state"] = "normal"
        self.csv_path_but["state"] = "normal"
        self.csv_path_tb["state"] = "normal"
        self.start_but["state"] = "normal"

    # Load raw CSV
    def load_raw_csv(self, csv_path:str) -> list[list[str]]:
        row_list = []

        with open(csv_path, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:
                row_list.append(row)

        return row_list

    # Clear and insert data to preview table
    def gen_file_list(self, detail_list):
        # Clear old data
        for item in self.file_list_tree.get_children():
            self.file_list_tree.delete(item)

        # Insert new data
        for row_detail in detail_list:
            self.file_list_tree.insert("", tk.END, values=row_detail)

    def convert_job(self):
        self.disable_all_but_field()
        self.start_but["text"] = "RUNNING"

        # Prepare list of data class
        img_list = []
        for file_detail in self.file_list_tree.get_children():
            detail_dict = self.file_list_tree.set(file_detail)
            img_obj = ImageDetailDec(file_path=os.path.join(self.pic_dir_tb.get(), detail_dict["img_name"]),
                                    lat_dec=float(detail_dict["lat_dec"]), long_dec=float(detail_dict["long_dec"]),
                                    altitude=float(detail_dict["alt"]))
            img_list.append(img_obj)

        # Edit GPS exif
        for img_obj in img_list:
            try:
                self.edit_gps_exif(img_obj)
            except Exception:
                print(f"ERROR while edit {img_obj.file_path}")

        self.enable_all_but_field()
        self.start_but["text"] = "START"
        self.sts_lb["text"] = ""
        tkMsgBox.showinfo(title="Process end", message="Finished insert GPS exif")

    def edit_gps_exif(self, img_obj:ImageDetailDec):
        def decimal_to_dms(decimal):
            d = int(decimal)
            m = int((decimal - d) * 60)
            s = (decimal - d - m/60) * 3600
            return (d, 1), (m, 1), (int(s * 100000), 100000)

        file_path = img_obj.file_path
        image_exist = os.path.exists(file_path)
        self.sts_lb["text"] = f"Editing {file_path}"
        if image_exist is True:
            exif_dict = piexif.load(file_path)
            exif_dict['GPS'][piexif.GPSIFD.GPSLatitude] = decimal_to_dms(img_obj.lat_dec)
            exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef] = "N" if img_obj.lat_dec >= 0 else "S"
            exif_dict['GPS'][piexif.GPSIFD.GPSLongitude] = decimal_to_dms(img_obj.long_dec)
            exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] = "E" if img_obj.long_dec >= 0 else "W"

            if img_obj.altitude >= 0:
                exif_dict['GPS'][piexif.GPSIFD.GPSAltitudeRef] = 0
            else:
                exif_dict['GPS'][piexif.GPSIFD.GPSAltitudeRef] = 1
            exif_dict['GPS'][piexif.GPSIFD.GPSAltitude] = ((int(abs(img_obj.altitude) * 10000), 10000))

            # Write the changes to the image
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, file_path)
            print(f"{file_path} edit ok")
        else:
            print(f"{file_path} is not exist, skip this entry")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
