from tkinter import *
import tkinter.messagebox

#*********Functions**********
def newfile():
    print("New Project Created")


window = Tk()

#********AppstartPopUps*******

tkinter.messagebox.showinfo('Pop up', "You need internet conection.")

answer = tkinter.messagebox.askquestion('Quiz',"Have you ever used ChatAPP")
if answer == 'yes':
    print("Welcome To Again, Sign In Here")
else:
    print("Would You like to SignUP")





#**********Menu**************
myMenu = Menu(window)
window.config(menu=myMenu)


filemenu = Menu(myMenu)
myMenu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New Project", command=newfile)

editmenu =Menu(myMenu)
myMenu.add_cascade(label="Edit", menu=editmenu)
editmenu.add_command(label="Undo", command=print("Undo"))
#*******End Of Menu**********



#***********TollBAr*****


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

tool5 = Button(myframe, text="text", bg="purple", fg="white")
tool5.pack(side=LEFT, padx=2, pady=2)

tool6 = Button(myframe, text="call", bg="purple", fg="white")
tool6.pack(side=LEFT, padx=2, pady=2)

tool7 = Button(myframe, text="video", bg="purple", fg="white")
tool7.pack(side=LEFT, padx=2, pady=2)

tool8 = Button(myframe, text="audio", bg="purple", fg="white")
tool8.pack(side=LEFT, padx=2, pady=2)

tool9 = Button(myframe, text="text", bg="purple", fg="white")
tool9.pack(side=LEFT, padx=2, pady=2)

tool10 = Button(myframe, text="call", bg="purple", fg="white")
tool10.pack(side=LEFT, padx=2, pady=2)

tool11 = Button(myframe, text="video", bg="purple", fg="white")
tool11.pack(side=LEFT, padx=2, pady=2)

tool12 = Button(myframe, text="audio", bg="purple", fg="white")
tool12.pack(side=LEFT, padx=2, pady=2)


#******End Of ToolBar***








#**********InsideApp**********
tos1 = Label(window, text="Welcome To ChatAPP" ,bg="red", fg="orange")
tos1.pack(fill=X)

tos2 = Label(window, text="The Best Way to CONNECT with Friends and Family \n We believe in Connections " ,bg="blue", fg="white")
tos2.pack(side=LEFT, fill=Y)

topFrame = Frame(window)
topFrame.pack(side=TOP)

bottomFrame = Frame(window)
bottomFrame.pack(side=BOTTOM)

goto = Button(topFrame, text="Click to Visit Webpage\n", fg="Blue")
label_1 = Label(window, text="Username")
entry_1 = Entry(window)
label_2 = Label(window, text="Password")
entry_2 = Entry(window, show="*")
checkBox = Checkbutton(window, text="Stay Logged in.")
signin = Button(window, text="Sign In", bg="blue", fg="white")
signup = Button(window, text="Sign up", bg="blue", fg="white")

goto.pack()
label_1.pack()
entry_1.pack()
label_2.pack()
entry_2.pack()
checkBox.pack()
signin.pack()
signup.pack()
# *********End of Insode App*********

#******StatusbaR********

status = Label(window, text="Nothings happening right now....", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

window.mainloop()