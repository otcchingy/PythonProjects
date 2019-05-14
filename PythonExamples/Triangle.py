import os


print("Welcome To Triangle Printer 1.0")

while True:
    def dtriangle():
        try:
            n = input("Input the Number of lines To Print or Press N To QUIT:  ") 
            if n.lower() == 'n':
                print("\nGoodbye")  
                os.system("pause")
            else:
                nn = int(n)
                t = str(input("What would you like your trianle made of(Press Enter To Use Default):   "))
                if t == "": 
                    t = str("@")
            #creating the triangle
                x = 0
                while x is not nn:
                    x += 1
                    nc = (len(t)) % 2
                    cc = len(t)
                    if nc == 0:
                        z = ((cc//2)+1)
                        triangle = ((str(" ")*z)*(nn - x)) + ((t+"  ") * x)
                        print(triangle)
                    else:
                        z = cc - ((cc-1)//2)
                        triangle = (str(" ")*z)*(nn - x) + ((t + " ") * x)
                        print(triangle)
            dtriangle()
        except Exception:
            print("Enter positive numbers only")
            dtriangle()
    dtriangle()



