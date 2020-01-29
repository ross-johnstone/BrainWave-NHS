from tkinter import Tk, Label, Button, Toplevel, Entry, PhotoImage
import tkinter
import matplotlib.pyplot as plt
import re
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.widgets import SpanSelector
from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch
import datetime
import numpy as np
import matplotlib
from tkinter import filedialog
from annotations import Annotation, save_json
import data


class TkBase:
    def __init__(self, master, times, values):

        FIGSIZE = (8, 3)

        self.master = master
        master.title("BrainWave Visualization")

        # list of all annotations
        self.data, self.timestamps, self.annotations = data.open_project('data/recording1/pat1/')

        # create a matplotlib figure with a single axes on which the data will be displayed
        self.fig, self.ax = plt.subplots(figsize=FIGSIZE)
        self.fig.set_facecolor('xkcd:grey')
        self.ax.set_facecolor('xkcd:dark grey')

        # plot values on the axe and set plot hue to NHS blue
        self.ax.plot(self.timestamps, self.data, color='#5436ff')
        # draw all saved annotations
        for annotation in self.annotations:
            self.draw_annotation(annotation)

        self.ax.xaxis_date()
        plt.gcf().autofmt_xdate()
        # adding grid
        self.ax.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
        # removing top and right borders
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

        line = self.ax.lines[0]

        # put the plot with navbar on the tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)
        self.canvas.mpl_connect('button_release_event', self.butrelease)

        self.toolbar = NavigationToolbar(self.canvas, root)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)

        # add span selector to the axes but set it defaultly to not visible,
        # only activate it when the button annotate is pressed
        self.span = SpanSelector(self.ax, self.onselect, 'horizontal', useblit=True,
                                 rectprops=dict(alpha=0.5, facecolor='red'), span_stays=True)
        self.span.set_visible(False)

        # second, reference graph displayed
        self.fig2, self.ax2 = plt.subplots(figsize=FIGSIZE)
        self.fig2.set_facecolor('xkcd:grey')
        self.ax2.plot(self.timestamps, self.data, color="cyan")
        self.ax2.set_facecolor('xkcd:dark grey')
        self.ax2.xaxis_date()

        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=root)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)

        # create buttons for interaction
        self.annotate_button = Button(master, command=self.annotate, text="Annotate",
                                      compound="left", font="Consolas")

        self.export_button = Button(master, command=self.export, text="Export to PDF",
                                    compound="left", font="Consolas")

        self.close_button = Button(master, command=master.quit, text="Quit", compound="left",
                                   font="Consolas")

        # variables for storing min and max of the current span selection
        self.span_min = None
        self.span_max = None

        # self.open_button = Button(master, text="Open", command=self.open, bg='white')
        # self.open_button.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

        master.iconbitmap(r'res/general_images/favicon.ico')
        master.state('zoomed')

    # callback method for the open button, opens an existing project
    def open(self):
        FIGSIZE = (8, 3)
        path = filedialog.askdirectory()
        path = path + "/"
        self.data, self.timestamps, self.annotations = data.open_project(path)

        self.ax.clear()
        self.ax.plot(self.timestamps, self.data, color='#5436ff')
        # draw all saved annotations
        for annotation in self.annotations:
            self.draw_annotation(annotation)

        self.ax.xaxis_date()
        plt.gcf().autofmt_xdate()
        # adding grid
        self.ax.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
        # removing top and right borders
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

        line = self.ax.lines[0]
        self.canvas.draw()

        self.ax2.clear()
        self.ax2.plot(self.timestamps, self.data)
        self.ax2.xaxis_date()

        self.canvas2.draw()
        self.canvas2.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)

    # callback method for the anotate button activates the span selector
    def butrelease(self, event):
        # deactivate toolbar functionalities if any are active
        if (self.toolbar._active == 'PAN'):
            self.toolbar.pan()

        if (self.toolbar._active == 'ZOOM'):
            self.toolbar.zoom()

    def compare(self):
        pass

    def export(self):
        plt.figure(1)
        plt.savefig('fig.pdf')

    def annotate(self):
        # activate the span selector
        self.span.set_visible(True)

        # deactivate toolbar functionalities if any are active
        if (self.toolbar._active == 'PAN'):
            self.toolbar.pan()

        if (self.toolbar._active == 'ZOOM'):
            self.toolbar.zoom()

        self.annotate_button.config(text='Confirm', command=self.confirm)

    # callback method for the annotate button after span is sellected this button
    # is pressed to add descriptions to the annotation and confirm selection
    def confirm(self):
        # if something is selected
        if (self.span_min):
            # method called when cancel button on popup is pressed
            def cancel():
                self.span_min = False
                top.destroy()
                top.update()

            # method called when save button on popup is pressed
            def save():
                if not title_entry.get().strip():
                    error_label = Label(top, text="Please add a title!", fg="red")
                    error_label.grid(row=3)
                else:
                    new_annotation = Annotation(title_entry.get(), description_entry.get(1.0, tkinter.END),
                                                self.span_min, self.span_max)

                    self.annotations.append(new_annotation)
                    save_json(self.annotations, 'data/recording1/pat1/annotations.json')
                    self.draw_annotation(new_annotation)

                    # set spans back to none after the annotation is saved to prevent buggy behavior
                    self.span_min = None
                    self.span_max = None

                    # destroy popup after annotation is saved
                    cancel()

            # create popup where you add text to the annotation
            top = Toplevel(root)
            top.title('Confirm Annotation')
            top.grab_set()

            # labels in top level window showing annotation start time and end time
            annotation_start_label = Label(top, text='Annotation start time: ' + str(self.span_min))
            annotation_end_label = Label(top, text='Annotation end time: ' + str(self.span_max))
            annotation_start_label.grid(row=0)
            annotation_end_label.grid(row=1)

            annotation_title_label = Label(top, text='Title')
            annotation_title_label.grid(row=2)
            title_entry = Entry(top, font=("Courier", 12))
            title_entry.grid(row=4)

            description_label = Label(top, text='Description')
            description_label.grid(row=5)
            description_entry = tkinter.Text(top, height=6, width=30)
            description_entry.grid(row=6)

            save_button = Button(master=top, text="Save", command=save, bg='white')
            save_button.grid(row=7)

            cancel_button = Button(master=top, text="Cancel", command=cancel, bg='white')
            cancel_button.grid(row=8)

            # change button back to annotate button and hide span selector again
            self.annotate_button.config(text='Annotate', command=self.annotate)
            self.span.set_visible(False)

            # hide the rectangle after confirm button is pressed
            self.span.stay_rect.set_visible(False)
            self.canvas.draw()

            top.resizable(False, False)
            top.iconbitmap(r"./res/general_images/favicon.ico")
            top.protocol("WM_DELETE_WINDOW", cancel)

    # callback method of the span selector, after every selection it writes
    # the selected range to class variables
    def onselect(self, min, max):
        self.span_min = datetime.datetime.fromordinal(int(min)) + datetime.timedelta(seconds=divmod(min, 1)[1] * 86400)
        self.span_max = datetime.datetime.fromordinal(int(max)) + datetime.timedelta(seconds=divmod(max, 1)[1] * 86400)

        # get vertical range for a given annotation

    def get_vertical_range(self, annotation):

        range_indices = np.where(np.logical_and(self.timestamps > annotation.start, self.timestamps < annotation.end))

        range_data = self.data[range_indices]
        return range_data[np.argmax(range_data)], range_data[np.argmin(range_data)]

    def draw_annotation(self, annotation):
        # if date range annotation draw rectangle
        if (annotation.start != annotation.end):
            vmax, vmin = self.get_vertical_range(annotation)
            tp = TextPath((matplotlib.dates.date2num(annotation.start) + 6000, 300), annotation.title, size=100000)
            self.ax.add_patch(PathPatch(tp, color="black"))
            self.ax.add_patch(plt.Rectangle((matplotlib.dates.date2num(annotation.start), vmin - 10),
                                            matplotlib.dates.date2num(annotation.end) - matplotlib.dates.date2num(
                                                annotation.start), vmax - vmin + 20, fc='r'))
        # if point annotation draw a vertical line
        if (annotation.start == annotation.end):
            plt.figure(1)
            plt.axvline(x=matplotlib.dates.date2num(annotation.start))
        self.fig.canvas.draw()


class NavigationToolbar(NavigationToolbar2Tk):

    def _Button(self, text, file, command, extension='.gif'):
        img_file = ("./res/button_images/" + file + extension)
        im = tkinter.PhotoImage(master=self, file=img_file)
        b = tkinter.Button(
            master=self, text=text, padx=2, pady=2, image=im, command=command)
        b._ntimage = im
        b.pack(side=tkinter.LEFT)
        return b

    toolitems = (
        ('Home', 'Reset original view', 'home', 'home'),
        ('Back', 'Back to previous view', 'back', 'back'),
        ('Forward', 'Forward to next view', 'forward', 'forward'),
        (None, None, None, None),
        ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
        ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
        ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
        (None, None, None, None),
        ('Annotate', 'Create an annotation', 'annotate', 'call_annotate'),
        ('Confirm', 'Confirm annotation', 'confirm', 'call_confirm'),
        (None, None, None, None),
        ('Open', 'Opens a new project', 'open', 'call_open'),
        ('Export', 'Export to PDF', 'export', 'call_export'),
        ('Save', 'Save the figure', 'filesave', 'save_figure'),
        (None, None, None, None),
        ('Quit', 'Quit application', 'quit', 'call_quit'),
    )

    def call_annotate(self):
        TkBase.annotate(my_gui)

    def call_confirm(self):
        TkBase.confirm(my_gui)

    def call_open(self):
        TkBase.open(my_gui)

    def call_export(self):
        TkBase.export(my_gui)

    def call_quit(self):
        root.quit()


root = Tk()
my_gui = TkBase(root, [datetime.datetime.now() - datetime.timedelta(hours=x) for x in range(10)],
                [1, 2, 3, 5, 3, 1, 8, 6, 4, 7])
root.mainloop()
