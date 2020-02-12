from tkinter import Label, Button, Toplevel, Entry, filedialog, PhotoImage
import tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.widgets import SpanSelector
from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch
from matplotlib.dates import date2num
import datetime
import numpy as np
from annotations import Annotation, save_json
import data
from tkinter import messagebox


class TkBase:

    def __init__(self, master, path):

        FIGSIZE = (8, 3)

        self.master = master

        master.title("BrainWave Visualization")

        # create matplotlib figures with single axes on which the data will be
        # displayed
        self.main_graph, self.main_graph_ax = plt.subplots(figsize=FIGSIZE)
        self.main_graph.set_facecolor('xkcd:grey')
        self.main_graph_ax.set_facecolor('xkcd:dark grey')

        # second, reference graph
        self.reference_graph, self.reference_graph_ax = plt.subplots(
            figsize=FIGSIZE)
        self.reference_graph.set_facecolor('xkcd:grey')
        self.reference_graph_ax.set_facecolor('xkcd:dark grey')
        self.main_canvas = FigureCanvasTkAgg(self.main_graph, master=master)
        self.main_canvas.get_tk_widget().pack(
            side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)
        self.toolbar = NavigationToolbar(
            self.main_canvas, self.master, tkbase_=self)

        self.reference_canvas = FigureCanvasTkAgg(
            self.reference_graph, master=master)
        self.reference_canvas.get_tk_widget().pack(
            side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)
        self.reference_canvas.get_tk_widget().pack(
            side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)

        self.project_path = path
        try:
            self.data, self.timestamps, self.annotations = data.open_project(
                self.project_path)
            self.draw_graph(self.data, self.timestamps, self.annotations)
        except Exception as e:
            messagebox.showerror("Error:", e)

        # put the plot with navbar on the tkinter window
        self.main_canvas.mpl_connect('button_release_event', self.butrelease)

        # add span selector to the axes but set it defaultly to not visible,
        # only activate it when the button annotate is pressed
        self.span = SpanSelector(self.main_graph_ax, self.onselect, 'horizontal', useblit=True,
                                 rectprops=dict(alpha=0.5, facecolor='red'), span_stays=True)
        self.span.set_visible(False)

        # create buttons for interaction
        self.annotate_button = Button(master, command=self.annotate)

        self.export_button = Button(master, command=self.export)

        self.close_button = Button(master, command=master.quit)

        # variables for storing min and max of the current span selection
        self.span_min = None
        self.span_max = None

    # callback method for the open button, opens an existing project
    def open(self):
        path = filedialog.askdirectory()
        path = path + "/"
        try:
            self.data, self.timestamps, self.annotations = data.open_project(
                path)
            self.draw_graph(self.data, self.timestamps, self.annotations)
        except Exception as e:
            messagebox.showerror("Error:", e)

    def open_concurrent(self):
        path = filedialog.askdirectory()
        path = path + "/"
        new_root = Toplevel(self.master)
        TkBase(new_root, path)

    # callback method for the annotate button activates the span selector
    def butrelease(self, event):
        # deactivate toolbar functionalities if any are active
        if (self.toolbar._active == 'PAN'):
            self.toolbar.pan()

        if (self.toolbar._active == 'ZOOM'):
            self.toolbar.zoom()

    def compare(self):
        pass

    def export(self):

        def cancel():
            self.span_min = False
            popup.destroy()
            popup.update()

        def save():
            filename = export_popup_entry.get() + '.pdf'
            with PdfPages(filename) as export_pdf:
                for i in plt.get_fignums()[::-1]:
                    plt.figure(i)
                    export_pdf.savefig()
            cancel()

        popup = Toplevel(self.master)
        popup.title('')
        popup.iconbitmap(r'res/general_images/favicon.ico')
        popup.grab_set()

        export_popup_label = Label(popup, text="Enter desired file name: ")
        export_popup_label.grid(row=0, column=0)

        export_popup_entry = Entry(popup)
        export_popup_entry.grid(row=0, column=1)

        close_export_popup_button = Button(popup, text="Confirm", command=save)
        close_export_popup_button.grid(row=1, column=1)

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
                    error_label = Label(
                        top, text="Please add a title!", fg="red")
                    error_label.grid(row=3)
                else:
                    new_annotation = Annotation(title_entry.get(), description_entry.get(1.0, tkinter.END),
                                                self.span_min, self.span_max)

                    self.annotations.append(new_annotation)
                    json_path = self.project_path + 'annotations.json'
                    save_json(self.annotations, json_path)
                    self.draw_annotation(new_annotation)

                    # set spans back to none after the annotation is saved to
                    # prevent buggy behavior
                    self.span_min = None
                    self.span_max = None

                    # destroy popup after annotation is saved
                    cancel()

            # create popup where you add text to the annotation
            top = Toplevel(self.master)
            top.title('Confirm Annotation')
            top.grab_set()

            # labels in top level window showing annotation start time and end
            # time
            annotation_start_label = Label(
                top, text='Annotation start time: ' + str(self.span_min))
            annotation_end_label = Label(
                top, text='Annotation end time: ' + str(self.span_max))
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

            save_button = Button(master=top, text="Save",
                                 command=save, bg='white')
            save_button.grid(row=7)

            cancel_button = Button(
                master=top, text="Cancel", command=cancel, bg='white')
            cancel_button.grid(row=8)

            # change button back to annotate button and hide span selector
            # again
            self.annotate_button.config(text='Annotate', command=self.annotate)
            self.span.set_visible(False)

            # hide the rectangle after confirm button is pressed
            self.span.stay_rect.set_visible(False)
            self.main_canvas.draw()

            top.resizable(False, False)
            top.iconbitmap(r"./res/general_images/favicon.ico")
            top.protocol("WM_DELETE_WINDOW", cancel)

    # callback method of the span selector, after every selection it writes
    # the selected range to class variables
    def onselect(self, min, max):
        self.span_min = datetime.datetime.fromordinal(
            int(min)) + datetime.timedelta(seconds=divmod(min, 1)[1] * 86400)
        self.span_max = datetime.datetime.fromordinal(
            int(max)) + datetime.timedelta(seconds=divmod(max, 1)[1] * 86400)

    # get vertical range for a given annotation
    def get_vertical_range(self, annotation):

        range_indices = np.where(np.logical_and(
            self.timestamps > annotation.start, self.timestamps < annotation.end))

        range_data = self.data[range_indices]
        return range_data[np.argmax(range_data)], range_data[np.argmin(range_data)]

    def draw_annotation(self, annotation):
        # if date range annotation draw rectangle
        if (annotation.start != annotation.end):
            vmax, vmin = self.get_vertical_range(annotation)
            tp = TextPath((date2num(annotation.start) + 6000, 300), annotation.title, size=100000)
            self.main_graph_ax.add_patch(PathPatch(tp, color="black"))
            self.main_graph_ax.add_patch(plt.Rectangle((date2num(annotation.start), vmin - 10),
                                                       date2num(annotation.end) - date2num(
                                                           annotation.start), vmax - vmin + 20, fc='r'))
        # if point annotation draw a vertical line
        if (annotation.start == annotation.end):
            plt.figure(1)
            plt.axvline(x=date2num(annotation.start))
        self.main_canvas.draw()

    def draw_graph(self, data, timestamps, annotations):
        self.main_graph_ax.clear()
        # plot values on the axe and set plot hue to NHS blue
        self.main_graph_ax.plot(timestamps, data, color='#5436ff')
        # draw all saved annotations
        for annotation in annotations:
            self.draw_annotation(annotation)

        self.main_graph_ax.xaxis_date()
        plt.gcf().autofmt_xdate()
        # adding grid
        self.main_graph_ax.grid(
            color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
        # removing top and right borders
        self.main_graph_ax.spines['top'].set_visible(False)
        self.main_graph_ax.spines['right'].set_visible(False)
        # put the plot with navbar on the tkinter window
        self.main_canvas.draw()

        self.toolbar.update()

        # second, reference graph displayed
        self.reference_graph_ax.clear()
        self.reference_graph_ax.plot(
            self.timestamps, self.data, color="cyan", linewidth=1)
        self.reference_graph_ax.xaxis_date()
        # put the second plot on the tkinter window
        self.reference_canvas.draw()

    def close(self):
        self.master.quit()


class NavigationToolbar(NavigationToolbar2Tk):

    def __init__(self, canvas_, parent_, tkbase_):
        self.tkbase_ = tkbase_
        self.parent_ = parent_
        self.toolitems = (
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
            ('Open Concurrent', 'Open a concurrent graph view',
             'compare', 'call_open_concurrent'),
            (None, None, None, None),
            ('Quit', 'Quit application', 'quit', 'call_quit'),
        )
        NavigationToolbar2Tk.__init__(self, canvas_, parent_)

    def _Button(self, text, file, command, extension='.gif'):
        img_file = ("./res/button_images/" + file + extension)
        im = PhotoImage(master=self, file=img_file)
        b = Button(
            master=self, text=text, padx=2, pady=2, image=im, command=command)
        b._ntimage = im
        b.pack(side=tkinter.LEFT)
        return b

    def call_annotate(self):
        TkBase.annotate(self.tkbase_)

    def call_confirm(self):
        TkBase.confirm(self.tkbase_)

    def call_open(self):
        TkBase.open(self.tkbase_)

    def call_open_concurrent(self):
        TkBase.open_concurrent(self.tkbase_)

    def call_export(self):
        TkBase.export(self.tkbase_)

    def call_quit(self):
        TkBase.close(self.tkbase_)


# root = Tk()
# my_gui = TkBase(root, [datetime.datetime.now() - datetime.timedelta(hours=x) for x in range(10)],
#                 [1, 2, 3, 5, 3, 1, 8, 6, 4, 7])
# root.mainloop()
