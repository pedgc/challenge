from tkinter import Tk, font
from tkinter import *
root = Tk()
root.geometry('300x600')
root.resizable(width=True,height=True)

tinfo = Text(root, width=25, height=30)
tinfo['font'] = "Helvetica"

fonts = font.families()
# Delete info of the textbox
tinfo.delete("1.0", END)
for f in fonts:
    tinfo.insert("1.0", str(f)+"\n")

tinfo.pack(side=TOP)
root.mainloop()
