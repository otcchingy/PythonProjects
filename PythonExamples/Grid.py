from tkinter import *

window = Tk()

tos1 = Label(window, text="Welcome To ChatAPP" ,bg="red", fg="orange")
tos1.grid(columnspan=2,rowspan=5)



label_1 = Label(window, text="Username")
label_2 = Label(window, text="Password")
entry_1 = Entry(window)
entry_2 = Entry(window)

label_1.grid(row=5)
label_2.grid(row=6)
entry_1.grid(row=5, column=1)
entry_2.grid(row=6, column=1)


c = Checkbutton(window, text="Stay Logged in.")
c.grid(columnspan=2)




window.mainloop()