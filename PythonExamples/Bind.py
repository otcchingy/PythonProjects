from tkinter import *

window = Tk()

#Fuctions
def leftclick(event):
    print("You Cicked Left")

def rightclick(event):
    print("You Cicked Right")



game_frame = Frame(window, width=350, height=450)
game_frame.bind("<Button-1>", leftclick)
game_frame.bind("<Button-3>", rightclick)
game_frame.pack()


window.mainloop()