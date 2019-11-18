from tkinter import *
from PIL import Image as Img
from PIL import ImageTk as Itk
from tkinter import Tk, Label, Button
import tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)


def app_screen():

    app_page = Tk()
    app_page.title("Graph Reader")

    times = [1, 2, 3]
    values = [1, 2, 3]

    # create a matplotlib figure with a single axes on which the data will be displayed
    fig, ax = plt.subplots()

    # plot values on the axes
    ax.plot(times, values)

    # put the plot with navbar on the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=app_page)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, app_page)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)

    def anotate():
        pass

    anotate_button = Button(app_page, text="anotate", command=anotate)
    anotate_button.pack()

    close_button = Button(app_page, text="Close", command=exit)
    close_button.pack()