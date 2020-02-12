import tkinter as tk
from tkinter import ttk, filedialog, messagebox, BOTTOM
from tkinterbase import TkBase
import re
import os


class HomePage:

    def __init__(self, master):
        # Initialises window with background image and widgets
        self.master = master
        master.title("BrainWave Visualization - HomePage")
        master.iconbitmap(r'res/general_images/favicon.ico')
        self.frame = tk.Frame(self.master)
        fname = r'res/general_images/homepage.png'
        self.bg_image = tk.PhotoImage(file=fname)
        # Centering window
        self.w = self.bg_image.width()
        self.h = self.bg_image.height()
        self.window_width = self.master.winfo_reqwidth()
        self.window_height = self.master.winfo_reqheight()
        self.x = (self.master.winfo_screenwidth() / 2) - (self.w / 2)
        self.y = (self.master.winfo_screenheight() / 2) - (self.h / 2)
        self.master.geometry("%dx%d+%d+%d" % (self.w, self.h, self.x, self.y))
        self.cv = tk.Canvas(width=self.w, height=self.h)
        self.cv.pack(side='top', fill='both', expand='yes')
        self.cv.create_image(0, 0, image=self.bg_image, anchor='nw')
        # Define buttons here
        self.open_button = ttk.Button(
            self.cv, text='Open', width=25, command=self.load_project)
        self.quit_button = ttk.Button(
            self.cv, text='Quit', width=25, command=self.close)
        # Buttons packed here - in descending order (Things at bottom will
        # appear at top)
        self.quit_button.pack(side=BOTTOM, padx=10, pady=25)
        self.open_button.pack(side=BOTTOM, padx=10, pady=25)
        self.frame.pack()

    def load_project(self):
        path = filedialog.askdirectory()
        if not path:
            # If user exits file directory  - shows error msg
            messagebox.showerror("Error", "File could not be opened.")
        else:
            path = path + "/"
            if not self.isValid(path):
                # If user picks a folder with no .cal or .wav files - shows
                # error msg
                messagebox.showerror("Error", "Inappropriate file type.")
            elif self.isValid(path):
                # Destroys homepage and runs main app
                self.open_button.destroy()
                self.quit_button.destroy()
                self.cv.destroy()
                my_gui = TkBase(root, path)
                root.resizable(True, True)

    def isValid(self, path):
        # Checks the path contents to see if it has .cal and .wav files
        contents = os.listdir(path)
        calfile=""
        datafiles=[]
        calfile = ""
        datafiles = []
        jsonfile = ""
        for filepath in contents:
            if re.match(r'\d{2}-\d{2}-\d{4}_\d{2}_\d{2}_\d{2}_\d{1,4}_\d*.cal', filepath):
                calfile = path + filepath
            elif re.match(r'\d{2}-\d{2}-\d{4}_\d{2}_\d{2}_\d{2}_\d{1,4}_\d*.wav', filepath):
                datafiles.append(path + filepath)
        if (calfile != "") and (datafiles != []):
            return True
        else:
            return False

    def close(self):
        # Pop up to user asking them if they want to quit
        if messagebox.askokcancel("", "Are you sure you want to quit?"):
            self.master.destroy()

root = tk.Tk()
root.resizable(False, False)
app = HomePage(root)
root.mainloop()