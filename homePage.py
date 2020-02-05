import tkinter as tk
from tkinterbase import *
import data
import os

class Demo1:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame, text = 'New Window', width = 25, command = self.open_project)
        self.button1.pack()
        self.frame.pack()

    def open_project(self):
        self.newWindow = tk.Toplevel(self.master)
        path = filedialog.askdirectory()
        path = path + "/"
        self.data, self.timestamps, self.annotations = data.open_project(path)
        self.app = TkBase(self.newWindow, self.data, self.timestamps)

root = tk.Tk()
app = Demo1(root)
root.mainloop()