import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinterbase import TkBase
import datetime

class HomePage:
    def __init__(self, master):
        self.master = master
        master.title("BrainWave Visualization - HomePage")
        master.iconbitmap(r'res/general_images/favicon.ico')
        self.frame = tk.Frame(self.master)
        fname=r'res/general_images/homepage.png'
        self.bg_image = tk.PhotoImage(file=fname)
        self.w = self.bg_image.width()
        self.h = self.bg_image.height()
        root.geometry("%dx%d+50+30" % (self.w,self.h))
        self.cv = tk.Canvas(width=self.w,height=self.h)
        self.cv.pack(side='top',fill='both',expand='yes')
        self.cv.create_image(0,0,image=self.bg_image,anchor='nw')
        self.button1 = ttk.Button(self.cv, text = 'Start', width = 25, command = self.new_project)
        self.button2 = ttk.Button(self.cv, text = 'Load', width=25, command = self.load_project)
        self.button3 = ttk.Button(self.cv, text = 'Quit', width=25, command = root.destroy)
        self.button3.pack(side=BOTTOM, padx=10, pady=25)
        self.button2.pack(side=BOTTOM, padx=10, pady=25)
        self.button1.pack(side=BOTTOM, padx=10, pady=25)
        self.frame.pack()

    def new_project(self):
        self.button1.destroy()
        self.button2.destroy()
        self.button3.destroy()
        self.cv.destroy()
        my_gui = TkBase(root, [datetime.datetime.now() - datetime.timedelta(hours=x) for x in range(10)],
                [1, 2, 3, 5, 3, 1, 8, 6, 4, 7])


    def load_project(self):
        self.button1.destroy()
        self.button2.destroy()
        self.button3.destroy()
        self.cv.destroy()
        my_gui = TkBase(root, [datetime.datetime.now() - datetime.timedelta(hours=x) for x in range(10)],
            [1, 2, 3, 5, 3, 1, 8, 6, 4, 7])
        my_gui.open()

root = tk.Tk()
app = HomePage(root)
root.mainloop()