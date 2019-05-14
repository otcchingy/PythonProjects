from tkinter import *


window = Tk()

photo = PhotoImage(file = "C:\PythonJunk\pappicon.png")
label =Label(window, image=photo)
label.pack()

window.mainloop()