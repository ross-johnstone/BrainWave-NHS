from tkinter import Tk, Label, Button, Toplevel, Entry
import tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.widgets import SpanSelector
from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch
import datetime
import numpy as np
import matplotlib
from annotations import Annotation, save_json
import data


class TkBase:
    def __init__(self, master, times, values):

        FIGSIZE = (8,3)

        self.master = master
        master.title("tkinter barebones")

        #list of all annotations
        self.data, self.timestamps, self.annotations = data.open_project('data/recording1/pat1/')

        # create a matplotlib figure with a single axes on which the data will be displayed
        self.fig, self.ax = plt.subplots(figsize = FIGSIZE)

        #plot values on the axe and set plot hue to NHS blue
        self.ax.plot(self.timestamps,self.data, color='#5436ff')

        #map from annotation id to the drawn shape in the graph
        self.id_to_shape = dict()

        #draw all saved annotations
        for annotation in self.annotations:
            self.draw_annotation(annotation)

        self.ax.xaxis_date()
        plt.gcf().autofmt_xdate()
        #adding grid
        self.ax.grid(color='grey',linestyle='-', linewidth=0.25, alpha=0.5)
        #removing top and right borders
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

        line = self.ax.lines[0]
        print(line.get_xdata())

        self.listbox_frame = tkinter.Frame(master)
        self.listbox_frame.pack(side=tkinter.RIGHT)

        #list to convert from indices in listbox to annotation ids
        self.index_to_ids = list()

        for id in self.annotations:
            id = id.id
            self.index_to_ids.append(id)


        self.listb = tkinter.Listbox(self.listbox_frame)
        for a in self.annotations:
            self.listb.insert(tkinter.END,a.title)
        self.listb.bind('<<ListboxSelect>>', self.listbox_selection)
        self.listb.grid(column=0,row=1)


        self.labelTitle = tkinter.Label(self.listbox_frame,
                            text = "Title:")
        self.labelTitle.grid(column=0, row=2)

        self.labelDescription = tkinter.Label(self.listbox_frame,
                            text = "description:",
                            wraplength=200)
        self.labelDescription.grid(column=0, row=3)

        self.go_to_annotation = tkinter.Button(self.listbox_frame,text='Go To annotation',command = self.goto_callback)
        self.go_to_annotation.grid(column=0, row=4)

        self.edit_annotation = tkinter.Button(self.listbox_frame,text='edit',command = self.edit_callback)
        self.edit_annotation.grid(column=0, row=5)

        self.delete_annotation = tkinter.Button(self.listbox_frame,text='delete',command = self.delete_callback)
        self.delete_annotation.grid(column=0, row=6)

        # put the plot with navbar on the tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)
        self.canvas.mpl_connect('button_release_event', self.butrelease)

        self.toolbar = NavigationToolbar2Tk(self.canvas, root)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)
        self.fig.canvas.toolbar.push_current()

        #add span selector to the axes but set it defaultly to not visible,
        #only activate it when the button annotate is pressed
        self.span = SpanSelector(self.ax, self.onselect, 'horizontal', useblit=True,
                                 rectprops=dict(alpha=0.5, facecolor='red'), span_stays=True)
        self.span.set_visible(False)

        # second, reference graph displayed
        self.fig2, self.ax2 = plt.subplots(figsize=FIGSIZE)
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

        #create buttons for interaction
        self.annotate_button = Button(master, text="Annotate", command=self.annotate, bg='white')
        self.annotate_button.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

        self.compare_button = Button(master, text="Export", command=self.export, bg='white')
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

    def export(self):
        plt.figure(1)
        plt.savefig('fig.pdf')

    #callback function for the listbox widget
    def listbox_selection(self,event):

        if(self.listb.curselection()):
            id = self.index_to_ids[self.listb.curselection()[0]]

            annotation = None

            for a in self.annotations:
                if a.id == id:

                    self.labelTitle['text'] = "Title: "+a.title
                    self.labelDescription['text'] = "Description: "+a.content

    #callback for go to annotation button
    def goto_callback(self):
        if(self.listb.curselection()):
            id = self.index_to_ids[self.listb.curselection()[0]]

            annotation = None

            for a in self.annotations:
                if a.id == id:

                    if(a.end != a.start):
                        range = self.get_vertical_range(a)
                        diff = (range[0]-range[1])/2
                        delta = (a.end - a.start)/15
                        self.ax.axis([a.start - delta, a.end + delta, range[1]-diff, range[0]+diff])

                    else:
                        delta = datetime.timedelta(seconds=10)
                        self.ax.axis([a.start - delta, a.end + delta, self.ax.get_ylim()[0], self.ax.get_ylim()[1]])
                    self.fig.canvas.toolbar.push_current()
                    self.fig.canvas.draw()


    def edit_callback(self):
        if(self.listb.curselection()):
            # method called when cancel button on popup is pressed
            def cancel():
                top.destroy()
                top.update()

            # method called when save button on popup is pressed
            def save():

                a.title = title_entry.get()
                a.content = description_entry.get()
                save_json(self.annotations,'data/recording1/pat1/annotations.json')
                self.listb.delete(index)
                self.listb.insert(index,title_entry.get())
                print(id)
                cancel()

            index = self.listb.curselection()[0]
            id = self.index_to_ids[self.listb.curselection()[0]]

            annotation = None

            for a in self.annotations:
                if a.id == id:
                    annotation = a
                    #popup in which you edit the annotation
                    top = Toplevel(root)
                    top.title('edit annotation')
                    top.grab_set()

                    #labels in top level window showing annotation start time and end time
                    annotation_start_label = Label(top,text='Annotation start time: '+str(a.start))
                    annotation_end_label = Label(top,text='Annotation end time: '+str(a.end))
                    annotation_start_label.pack()
                    annotation_end_label.pack()

                    title_entry = Entry(top)
                    title_entry.insert(tkinter.END,a.title)
                    title_entry.pack()

                    description_entry = Entry(top)
                    description_entry.insert(tkinter.END,a.content)
                    description_entry.pack()

                    cancel_button = Button(master=top, text = "Cancel",command = cancel, bg='white')
                    cancel_button.pack()

                    save_button = Button(master=top, text = "Save", command= save, bg='white')
                    save_button.pack()

    def delete_callback(self):
        if(self.listb.curselection()):
            index = self.listb.curselection()[0]
            id = self.index_to_ids[self.listb.curselection()[0]]

            annotation = None

            for a in self.annotations:
                if a.id == id:
                    self.index_to_ids.remove(id)
                    self.annotations.remove(a)
                    self.id_to_shape[id].remove()
                    del self.id_to_shape[id]
                    self.fig.canvas.draw()
                    save_json(self.annotations,'data/recording1/pat1/annotations.json')
                    self.listb.delete(index)


    def annotate(self):

        # activate the span selector
        self.span.set_visible(True)

        # deactivate toolbar functionalities if any are active
        if (self.toolbar._active == 'PAN'):
            self.toolbar.pan()

        if (self.toolbar._active == 'ZOOM'):
            self.toolbar.zoom()

        self.annotate_button.config(text='confirm', command=self.confirm)

        self.annotate_button.config(text='Confirm',command = self.confirm)

    #callback method for the annotate button after span is sellected this button
    #is pressed to add descriptions to the annotation and confirm selection
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
                save_json(self.annotations,'data/recording1/pat1/annotations.json')
                self.draw_annotation(new_annotation)
                self.index_to_ids.append(new_annotation.id)
                self.listb.insert(tkinter.END,new_annotation.title)

                #set spans back to none after the annotation is saved to prevent buggy behavior
                self.span_min=None
                self.span_max=None

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

        #get vertical range for a given annotation
    def get_vertical_range(self,annotation):

        range_indices = np.where(np.logical_and(self.timestamps>annotation.start,self.timestamps<annotation.end))

        range_data = self.data[range_indices]
        return range_data[np.argmax(range_data)], range_data[np.argmin(range_data)]

    def draw_annotation(self,annotation):
        #if date range annotation draw rectangle
        if(annotation.start != annotation.end):
            vmax,vmin = self.get_vertical_range(annotation)
            self.id_to_shape[annotation.id] = self.ax.add_patch(plt.Rectangle((matplotlib.dates.date2num(annotation.start),vmin-10),
                                             matplotlib.dates.date2num(annotation.end)-matplotlib.dates.date2num(annotation.start),vmax-vmin+20,fc='r'))
        #if point annotation draw a vertical line
        if(annotation.start==annotation.end):
            plt.figure(1)
            self.id_to_shape[annotation.id] = plt.axvline(x=matplotlib.dates.date2num(annotation.start))
        self.fig.canvas.draw()

root = Tk()
my_gui = TkBase(root, [datetime.datetime.now() - datetime.timedelta(hours=x) for x in range(10)],
                [1, 2, 3, 5, 3, 1, 8, 6, 4, 7])
root.mainloop()
