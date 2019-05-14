from tkinter import *


class myfunction:
    def __init__(self, main):
        frame = Frame(main)
        frame.pack()

        self.click = Button(frame, text="Click It", command=self.print_it)
        self.exitx = Button(frame, text="Quit", command=frame.quit)
        self.click.pack(side=LEFT)
        self.exitx.pack(side=LEFT)


    def print_it(self):
        print("Yaayy, You Clicked It..")


window = Tk()

app = myfunction(window)

window.mainloop()