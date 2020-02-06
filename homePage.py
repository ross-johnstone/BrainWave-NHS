import tkinter as tk
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
        os.system('tkinterbase.py')

root = tk.Tk()
app = Demo1(root)
root.mainloop()