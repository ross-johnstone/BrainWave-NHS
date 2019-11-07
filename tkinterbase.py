from tkinter import Tk, Label, Button, Toplevel
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
        self.fig, self.ax = plt.subplots()

        #plot values on the axes
        self.ax.plot(times,values)

        #put the plot with navbar on the tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)

        self.toolbar = NavigationToolbar2Tk(self.canvas, root)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)

        #add span selector to the axes but set it defaultly to not visible,
        #only activate it when the button anotte is pressed
        self.span = SpanSelector(self.ax, self.onselect, 'horizontal', useblit=True,
                rectprops=dict(alpha=0.5, facecolor='red'),span_stays=True)
        self.span.set_visible(False)


        #variables for storing min and max of the current span selection
        self.span_min=-1
        self.span_max=-1


        #create buttons for interaction
        self.anotate_button = Button(master, text="anotate", command=self.anotate)
        self.anotate_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    #callback method for the anotate button activates the span selector
    def anotate(self):

        #activate the span selector
        self.span.set_visible(True)

        self.anotate_button.config(text='confirm',command = self.confirm)

    #callback method for the anotate button after span is sellected this button
    #is pressed to add descriptions to the anotation and confirm selection
    def confirm(self):

        print(self.span_min,self.span_max)

        #save the anotation somewhere

        #create popup where you add text to the anotation
        top = Toplevel(root)
        top.grab_set()


        #change button back to anotate button and hide span selector again
        self.anotate_button.config(text='anotate',command=self.anotate)
        self.span.set_visible(False)

        #hide the rectagle after confirm button is pressed
        self.span.stay_rect.set_visible(False)
        self.canvas.draw()

    #callback method of the span selector, after every selection it writes
    #the selected range to class variables
    def onselect(self,min,max):
        self.span_min = min
        self.span_max = max

root = Tk()
my_gui = TkBase(root,[1,2,3],[1,2,3])
root.mainloop()
