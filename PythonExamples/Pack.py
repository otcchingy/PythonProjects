from tkinter import *


#*********Functions**********
def newfile():
    print("New Project Created")


window = Tk()

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
entry_2 = Entry(window)
checkBox = Checkbutton(window, text="Stay Logged in.")
signin = Button(bottomFrame, text="Sign In", bg="blue", fg="white")
signup = Button(bottomFrame, text="Sign up", bg="blue", fg="white")

goto.pack()
label_1.pack()
entry_1.pack()
label_2.pack()
entry_2.pack()
checkBox.pack()
signin.pack()
signup.pack()
# *********End of Insode App*********



window.mainloop()