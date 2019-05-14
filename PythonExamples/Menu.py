from tkinter import *

def newfile():
    print("New Project Created")



window = Tk()

myMenu = Menu(window)
window.config(menu=myMenu)


filemenu = Menu(myMenu)
myMenu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New Project", command=newfile)

filemenu.add_command(label="New", command=print("New File Opened"))
filemenu.add_command(label="Open Progect", command=print("New File Created"))
filemenu.add_separator()
filemenu.add_command(label="Save", command=print("File Save"))
filemenu.add_command(label="Save As", command=print("Save As what Name"))
filemenu.add_command(label="Import", command=print("Imported"))
filemenu.add_command(label="Export", command=print("Exported"))
filemenu.add_separator()
filemenu.add_command(label="Power Saver Mode", command=print("Saving Power"))
filemenu.add_command(label="Exit", command=print("CLOSED"))



editmenu =Menu(myMenu)
myMenu.add_cascade(label="Edit", menu=editmenu)
editmenu.add_command(label="Undo", command=print("Undo"))
editmenu.add_command(label="Redo", command=print("Redo"))
editmenu.add_separator()
editmenu.add_command(label="Copy", command=print("Copy"))
editmenu.add_command(label="Cut", command=print("Cut"))
editmenu.add_command(label="Paste", command=print("Paste"))

#******ToolBar********

myframe = Frame(window, bg="black")
myframe.pack(side=TOP, fill=X)

tool1 = Button(myframe, text="text", bg="purple", fg="white")
tool1.pack(side=LEFT, padx=2, pady=2)

tool2 = Button(myframe, text="call", bg="purple", fg="white")
tool2.pack(side=LEFT, padx=2, pady=2)

tool3 = Button(myframe, text="video", bg="purple", fg="white")
tool3.pack(side=LEFT, padx=2, pady=2)

tool4 = Button(myframe, text="audio", bg="purple", fg="white")
tool4.pack(side=LEFT, padx=2, pady=2)



#******StatusbaR********

status = Label(window, text="Nothings happening right now....", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)



window.mainloop()