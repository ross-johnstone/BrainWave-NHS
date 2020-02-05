import tkinter as tk
from tkinter import ttk
import data

def listbox_selection(event):
    id = index_to_ids[listb.curselection()[0]]

    annotation = None

    for a in annotations:
        if a.id == id:

            labelTitle['text'] = "Title: "+a.title
            labelDescription['text'] = "Description: "+a.content



app = tk.Tk()
app.geometry('200x500')

labelTop = tk.Label(app,
                    text = "Choose your favourite month")
labelTop.grid(column=0, row=0)

data, timestamps, annotations = data.open_project('data/recording1/pat1/')

#dicitonary to convert from indices in listbox to annotation ids
index_to_ids = dict()

for i,id in enumerate(annotations):
    id = id.id
    index_to_ids[i] = id


listb = tk.Listbox(app)
for a in annotations:
    listb.insert(tk.END,a.title)
listb.grid(column=0,row=1)
listb.bind('<<ListboxSelect>>', listbox_selection)

labelTitle = tk.Label(app,
                    text = "Title:")
labelTitle.grid(column=0, row=2)

labelDescription = tk.Label(app,
                    text = "description:",
                    wraplength=200)
labelDescription.grid(column=0, row=3)



app.mainloop()
