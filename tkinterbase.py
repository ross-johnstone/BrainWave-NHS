from tkinter import Tk, Label, Button
import tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.widgets import SpanSelector
import numpy as np


class TkBase:
    def __init__(self, master,times,values):
        self.master = master
        master.title("tkinter barebones")

        #create a matplotlib figure with a single axes on which the data will be displayed
        fig, ax = plt.subplots()

        #plot values on the axes
        ax.plot(times,values)

        #put the plot with navbar on the tkinter window
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, root)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)


        self.anotate_button = Button(master, text="anotate", command=self.anotate)
        self.anotate_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def anotate(self):
        pass

root = Tk()
my_gui = TkBase(root,[1,2,3],[1,2,3])
root.mainloop()
