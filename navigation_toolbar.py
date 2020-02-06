import tkinter as tk
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from tkinterbase import TkBase, my_gui


class NavigationToolbar(NavigationToolbar2Tk):

    def _Button(self, text, file, command, extension='.gif'):
        img_file = ("./res/button_images/" + file + extension)
        im = tk.PhotoImage(master=self, file=img_file)
        b = tk.Button(
            master=self, text=text, padx=2, pady=2, image=im, command=command)
        b._ntimage = im
        b.pack(side=tk.LEFT)
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
        ('Open Concurrent', 'Open a concurrent graph view', 'compare', 'call_open_concurrent'),
        (None, None, None, None),
        ('Quit', 'Quit application', 'quit', 'call_quit'),
    )

    def call_annotate(self):
        TkBase.annotate(my_gui)

    def call_confirm(self):
        TkBase.confirm(my_gui)

    def call_open(self):
        TkBase.open(my_gui)

    def call_open_concurrent(self):
        TkBase.open_concurrent(my_gui)

    def call_export(self):
        TkBase.export(my_gui)

    def call_quit(self):
        TkBase.close(my_gui)
