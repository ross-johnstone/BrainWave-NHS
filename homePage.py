import tkinter as tk
from tkinter import ttk, filedialog, messagebox, BOTTOM
from tkinterbase import TkBase
from data import check_valid_path

default_toolitems = (
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
    ('Save', 'Save the graph as PNG', 'filesave', 'save_figure'),
    ('Open Concurrent', 'Open a concurrent graph view',
     'compare', 'call_open_concurrent'),
    (None, None, None, None),
    ('Quit', 'Quit application', 'quit', 'call_quit'),
)


class HomePage:

    def __init__(self, master):
        # Initialises window with background image and widgets
        self.master = master
        master.title("BrainWave Visualization - HomePage")
        master.iconbitmap(r'res/general_images/favicon.ico')
        self.frame = tk.Frame(self.master)
        fname = r'res/general_images/homepage.png'
        self.bg_image = tk.PhotoImage(file=fname)
        # Centering window
        self.w = self.bg_image.width()
        self.h = self.bg_image.height()
        self.window_width = self.master.winfo_reqwidth()
        self.window_height = self.master.winfo_reqheight()
        self.x = (self.master.winfo_screenwidth() / 2) - (self.w / 2)
        self.y = (self.master.winfo_screenheight() / 2) - (self.h / 2)
        self.master.geometry("%dx%d+%d+%d" % (self.w, self.h, self.x, self.y))
        self.cv = tk.Canvas(width=self.w, height=self.h)
        self.cv.pack(side='top', fill='both', expand='yes')
        self.cv.create_image(0, 0, image=self.bg_image, anchor='nw')
        # Define buttons here
        self.open_button = ttk.Button(
            self.cv, text='Open', width=25, command=self.load_project)
        self.quit_button = ttk.Button(
            self.cv, text='Quit', width=25, command=self.close)
        # Buttons packed here - in descending order (Things at bottom will
        # appear at top)
        self.quit_button.pack(side=BOTTOM, padx=10, pady=25)
        self.open_button.pack(side=BOTTOM, padx=10, pady=25)
        self.frame.pack()

    def load_project(self):
        path = filedialog.askdirectory()
        if not path:
            # If user exits file directory  - do nothing
            pass
        else:
            path = path + "/"
            try:
                if check_valid_path(path):
                    # Destroys homepage and runs main app
                    self.open_button.destroy()
                    self.quit_button.destroy()
                    self.cv.destroy()
                    TkBase(root, path, default_toolitems)
                    root.resizable(True, True)
                    root.configure(bg="#949494")
            except Exception as e:
                # If user picks a folder with no .cal or .wav files - shows
                # error msg
                messagebox.showerror("Error", "Inappropriate file type.")

    def close(self):
        # Pop up to user asking them if they want to quit
        if messagebox.askokcancel("", "Are you sure you want to quit?"):
            self.master.destroy()


root = tk.Tk()
root.resizable(False, False)
app = HomePage(root)
root.mainloop()
