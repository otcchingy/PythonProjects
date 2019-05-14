from tkinter import *
import tkinter.messagebox



window = Tk()

tkinter.messagebox.showinfo('Pop up', "You need internet conection.")

answer = tkinter.messagebox.askquestion('Quiz',"Have you ever used ChatAPP")
if answer == 'yes':
    print("Welcome To Again, Sign In Here")
else:
    print("Would You like to SignUP")


window.mainloop()