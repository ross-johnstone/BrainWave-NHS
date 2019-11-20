from tkinter import *
from PIL import Image as Img
from PIL import ImageTk as Itk
from tkinter import Tk, Label, Button
import tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import graphApp


def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func


def login_page_screen():
    login_page = Tk()   # GUI Window
    login_page.geometry("300x500+500+100")  # Size of the window
    login_page.title("User Login")  # Title of the window

    # add background image
    original_bg = Itk.PhotoImage(Img.open("login_bg.png"))
    bg_label = Label(image=original_bg, bd="0")
    bg_label.place(x=-28, y=0)

    # add text entries2
    username_entry = Entry(master=login_page, width="16", exportselection=0, font=22)
    username_entry.place(x=51, y=180)

    password_entry = Entry(master=login_page, width="16", show="*", exportselection=0, font=22)
    password_entry.place(x=52, y=240)

    # create a Quit button
    quit_img = PhotoImage(file="quit_button.png")
    quit_button = Button(text="Quit", width="13", foreground="red", command=login_page.destroy,
                         font=("Consolas", 15), activeforeground="red")
    quit_button.place(x=73, y=430)

    # create a Sign Up button
    def signup_screen():
        signup_page = Tk()
        signup_page.geometry("300x500+500+100")
        signup_page.title("Sign Up")

        signup_bg = Itk.PhotoImage(Img.open("bg_img.jpg"), master=signup_page)
        signup_bg_label = Label(signup_page, image=signup_bg)
        signup_bg_label.place(x=-28, y=0)

        signup_quit_button = Button(signup_page, text="Quit", width="13", foreground="red", command=signup_page.destroy,
                             font=("Consolas", 15), activeforeground="red")
        signup_quit_button.place(x=73, y=430)

        signup_page.mainloop()

    signup_button = Button(text="Sign Up", width="10", command=signup_screen, font=("Consolas", 10))
    signup_button.place(x=168, y=365)

    # create a Login button

    login_button = Button(text="Login", width="17", command=combine_funcs(login_page.destroy, graphApp.app_screen),
                          font=("Consolas", 15))
    login_button.place(x=52, y=292)  # (x=55, y=365)

    login_page.mainloop()   # Start the GUI


login_page_screen()

