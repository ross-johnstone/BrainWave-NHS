import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
from tkinterbase import TkBase


class HomePage:
    def __init__(self, master):
        self.master = master
        master.title("BrainWave Visualization - HomePage")
        master.iconbitmap(r'res/general_images/favicon.ico')
        self.frame = tk.Frame(self.master)
        fname = r'res/general_images/homepage.png'
        self.bg_image = tk.PhotoImage(file=fname)
        self.w = self.bg_image.width()
        self.h = self.bg_image.height()
        self.window_width = self.master.winfo_reqwidth()
        self.window_height = self.master.winfo_reqheight()
        self.x = (self.master.winfo_screenwidth()/2) - (self.w/2)
        self.y = (self.master.winfo_screenheight()/2) - (self.h/2)
        self.master.geometry("%dx%d+%d+%d" % (self.w, self.h, self.x, self.y))
        self.cv = tk.Canvas(width=self.w, height=self.h)
        self.cv.pack(side='top', fill='both', expand='yes')
        self.cv.create_image(0, 0, image=self.bg_image, anchor='nw')
        self.open_button = ttk.Button(self.cv, text='Open', width=25, command=self.load_project)
        self.quit_button = ttk.Button(self.cv, text='Quit', width=25, command=root.destroy)
        self.quit_button.pack(side=BOTTOM, padx=10, pady=25)
        self.open_button.pack(side=BOTTOM, padx=10, pady=25)
        self.frame.pack()

    def load_project(self):
        path = filedialog.askdirectory()
        path = path + "/"
        self.open_button.destroy()
        self.quit_button.destroy()
        self.cv.destroy()
        my_gui = TkBase(root,path)
        root.resizable(True, True)



root = tk.Tk()
root.resizable(False, False)
app = HomePage(root)
root.mainloop()
