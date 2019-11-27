from tkinter import Tk, Label, Button, Toplevel, Entry
import tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.widgets import SpanSelector
import datetime
import numpy as np
import matplotlib
from annotations import Annotation
import data


class TkBase:
    def __init__(self, master, times, values):
        self.master = master
        master.title("tkinter barebones")

        #list of all annotations
        self.data, self.timestamps, self.annotations = data.open_project('data/pat1/')

        # create a matplotlib figure with a single axes on which the data will be displayed
        self.fig, self.ax = plt.subplots()

        #plot values on the axe and set plot hue to NHS blue
        self.ax.plot(self.timestamps,self.data, color='#5436ff')
        self.ax.xaxis_date()
        plt.gcf().autofmt_xdate()
        #adding grid
        self.ax.grid(color='grey',linestyle='-', linewidth=0.25, alpha=0.5)
        #removing top and right borders
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

        line = self.ax.lines[0]
        print(line.get_xdata())

        # put the plot with navbar on the tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)
        self.canvas.mpl_connect('button_release_event', self.butrelease)

        self.toolbar = NavigationToolbar2Tk(self.canvas, root)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)

        #add span selector to the axes but set it defaultly to not visible,
        #only activate it when the button annotate is pressed
        self.span = SpanSelector(self.ax, self.onselect, 'horizontal', useblit=True,
                                 rectprops=dict(alpha=0.5, facecolor='red'), span_stays=True)
        self.span.set_visible(False)

        # second, reference graph displayed
        self.fig2, self.ax2 = plt.subplots()
        self.ax2.plot(self.timestamps, self.data)
        self.ax2.xaxis_date()

        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=root)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)

        # variables for storing min and max of the current span selection
        self.span_min = None
        self.span_max = None

        #variables for storing min and max of the current span selection
        self.span_min=None
        self.span_max=None

        self.display_annotations = Label(master, text = self.annotations,wraplength=300)
        self.display_annotations.pack()

        #create buttons for interaction
        self.annotate_button = Button(master, text="Annotate", command=self.annotate, bg='white')
        self.annotate_button.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

        self.compare_button = Button(master, text="Compare", command=self.compare, bg='white')
        self.compare_button.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

        self.close_button = Button(master, text="Quit", command=master.quit, bg='white')
        self.close_button.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

    #callback method for the annotate button activates the span selector
    def butrelease(self,event):
        #deactivate toolbar functionalities if any are active
        if(self.toolbar._active=='PAN'):
            self.toolbar.pan()

        if (self.toolbar._active == 'ZOOM'):
            self.toolbar.zoom()

    def compare(self):
        pass

    def annotate(self):

        # activate the span selector
        self.span.set_visible(True)

        # deactivate toolbar functionalities if any are active
        if (self.toolbar._active == 'PAN'):
            self.toolbar.pan()

        if (self.toolbar._active == 'ZOOM'):
            self.toolbar.zoom()

        self.anotate_button.config(text='confirm', command=self.confirm)

        self.annotate_button.config(text='Confirm',command = self.confirm)

    #callback method for the annotate button after span is sellected this button
    #is pressed to add descriptions to the anontation and confirm selection
    def confirm(self):
        # if something is selected
        if (self.span_min):
            print(self.span_min, self.span_max)

            # method called when cancel button on popup is pressed
            def cancel():
                top.destroy()
                top.update()

            # method called when save button on popup is pressed
            def save():
                #new_annotation = Annotation(title_entry.text)
                print(title_entry.get())
                print(description_entry.get())

                new_annotation = Annotation(title_entry.get(),description_entry.get(),self.span_min,self.span_max)

                self.annotations.append(new_annotation)

                self.display_annotations['text'] = self.annotations
                #set spans back to none after the annotation is saved to prevent buggy behavior
                self.span_min=None
                self.span_max=None
                print(new_annotation)
                #destroy popup after annotation is saved
                cancel()

            #create popup where you add text to the annotation
            top = Toplevel(root)
            top.title('Confirm Annotation')
            top.grab_set()

            #labels in top level window showing annotation start time and end time
            annotation_start_label = Label(top,text='Annotation start time: '+str(self.span_min))
            annotation_end_label = Label(top,text='Annotation end time: '+str(self.span_max))
            annotation_start_label.pack()
            annotation_end_label.pack()

            title_entry = Entry(top)
            title_entry.pack()

            description_entry = Entry(top)
            description_entry.pack()

            cancel_button = Button(master=top, text = "Cancel",command = cancel, bg='white')
            cancel_button.pack()

            save_button = Button(master=top, text = "Save", command= save, bg='white')
            save_button.pack()



            #change button back to annotate button and hide span selector again
            self.annotate_button.config(text='Annotate',command=self.annotate)
            self.span.set_visible(False)

            # hide the rectagle after confirm button is pressed
            self.span.stay_rect.set_visible(False)
            self.canvas.draw()

    # callback method of the span selector, after every selection it writes
    # the selected range to class variables
    def onselect(self, min, max):
        print(datetime.datetime.fromordinal(int(min)) + datetime.timedelta(seconds=divmod(min, 1)[1] * 86400))
        print(datetime.datetime.fromordinal(int(max)) + datetime.timedelta(seconds=divmod(max, 1)[1] * 86400))
        self.span_min = datetime.datetime.fromordinal(int(min)) + datetime.timedelta(seconds=divmod(min, 1)[1] * 86400)
        self.span_max = datetime.datetime.fromordinal(int(max)) + datetime.timedelta(seconds=divmod(max, 1)[1] * 86400)


root = Tk()
my_gui = TkBase(root, [datetime.datetime.now() - datetime.timedelta(hours=x) for x in range(10)],
                [1, 2, 3, 5, 3, 1, 8, 6, 4, 7])
root.mainloop()