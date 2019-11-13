from tkinter import Tk, Label, Button, Toplevel, Entry
import tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.widgets import SpanSelector
import datetime
import numpy as np
import matplotlib


class TkBase:
    def __init__(self, master,times,values):
        self.master = master
        master.title("tkinter barebones")

        #create a matplotlib figure with a single axes on which the data will be displayed
        self.fig, self.ax = plt.subplots()

        #plot values on the axes
        self.ax.plot(times,values)
        self.ax.xaxis_date()
        plt.gcf().autofmt_xdate()

        line = self.ax.lines[0]
        print(line.get_xdata())

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
        self.span_min=None
        self.span_max=None


        #create buttons for interaction
        self.anotate_button = Button(master, text="anotate", command=self.anotate)
        self.anotate_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    #callback method for the anotate button activates the span selector
    def anotate(self):

        #activate the span selector
        self.span.set_visible(True)

        #deactivate toolbar functionalities if any are active
        if(self.toolbar._active=='PAN'):
            self.toolbar.pan()

        if(self.toolbar._active=='ZOOM'):
            self.toolbar.zoom()


        self.anotate_button.config(text='confirm',command = self.confirm)

    #callback method for the anotate button after span is sellected this button
    #is pressed to add descriptions to the anotation and confirm selection
    def confirm(self):
        #if something is selected
        if(self.span_min):
            print(self.span_min,self.span_max)

            #save the anotation somewhere

            #create popup where you add text to the anotation
            top = Toplevel(root)
            top.title('confirm anotation')
            top.grab_set()

            #labels in top level window showing anotation start time and end time
            anotation_start_label = Label(top,text='anotation start time: '+str(self.span_min))
            anotation_end_label = Label(top,text='anotation end time: '+str(self.span_max))
            anotation_start_label.pack()
            anotation_end_label.pack()

            title_entry = Entry(top)
            title_entry.pack()

            description_entry = Entry(top)
            description_entry.pack()



            #change button back to anotate button and hide span selector again
            self.anotate_button.config(text='anotate',command=self.anotate)
            self.span.set_visible(False)

            #hide the rectagle after confirm button is pressed
            self.span.stay_rect.set_visible(False)
            self.canvas.draw()

            self.span_min=None
            self.span_max=None



    #callback method of the span selector, after every selection it writes
    #the selected range to class variables
    def onselect(self,min,max):
        print(datetime.datetime.fromordinal(int(min))+datetime.timedelta(seconds=divmod(min,1)[1]*86400))
        print(datetime.datetime.fromordinal(int(max))+datetime.timedelta(seconds=divmod(max,1)[1]*86400))
        self.span_min = datetime.datetime.fromordinal(int(min))+datetime.timedelta(seconds=divmod(min,1)[1]*86400)
        self.span_max = datetime.datetime.fromordinal(int(max))+datetime.timedelta(seconds=divmod(max,1)[1]*86400)

root = Tk()
my_gui = TkBase(root,[datetime.datetime.now() - datetime.timedelta(hours=x) for x in range(10)],[1,2,3,5,3,1,8,6,4,7])
root.mainloop()
