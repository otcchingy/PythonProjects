import os
import string
from random import *

print("Abandant Grace Login")
username = ["Jacob", "Kwame", "Chingy", "Chris", "Dennis"]
password = ["Asdwe", "Tooknow", "Hilo", "kilo", "piusah604"]
adminlist = ["Admin", "Keysecret"]
firstname = []
lastname = []
dob = []
phone = []
passkey = 1232


def login(idname=input("Name ID  : "), passw=input("Password : ")):
    if idname in username and passw in password:
        print("Welcome",idname)
        os.system("pause")
    elif idname and passw in adminlist:
        print("Welcome Admin")
        os.system("pause")
    else:
        print("Invalid Login, Password Or ID incorrect")
        print("Do you want To Sign Up")
        answer = str(input("Press Y/N =  "))
        if answer.lower() == "y":
            key = int(input("Enter Signup Authourization Key =  "))
            if key == passkey:
                print("Welcome to SIGNUP")
                def signup():
                    print("Enter Your Information")
                    fname = str(input("Fistname: "))
                    lname = str(input("Lastname: "))
                    dobt = str(input("Date of Birth(DdMmYYYY): "))
                    phon = str(input("Phone Number: "))
                    usern = str(input("Username: "))
                    genpass = str(input("Do You want me to Generate A password For You(Y/N): "))
                    if genpass.lower() == "y":
                        characters = string.ascii_letters + string.punctuation + string.digits
                        passwrd = "".join(choice(characters) for x in range(randint(8, 16)))
                        password.append(passwrd)
                        print("Your password is " + passwrd)
                        print("Be sure to WRITE IT DOWN somewhere SAFE")
                        os.system("pause")
                        login(idname=input("Name ID  : "), passw=input("Password : "))
                    elif genpass.lower() == "n":
                        passwrd = str(input("Password: "))
                        repasswrd = str(input("Confirm Passowrd: "))
                        if passwrd == repasswrd:
                                    firstname.append(fname)
                                    lastname.append(lname)
                                    dob.append(dobt)
                                    phone.append(phon)
                                    username.append(usern)
                                    password.append(passwrd)
                                    print("You've Succesfully Created An Account")
                                    os.system("pause")
                                    login(idname=input("Name ID  : "), passw=input("Password : "))
                        else:
                                print("Passwords Don't Match Try again")
                                while passwrd != repasswrd:
                                    passwrd = str(input("Password: "))
                                    repasswrd = str(input("Confirm Passowrd: "))
                                    print("You've Succesfully Created An Account")
                                    os.system("pause")
                                    login(idname=input("Name ID  : "), passw=input("Password : "))

                    else:
                        print("Enter A valid Answer")
                        while genpass.lower() != "n" or genpass.lower() != "y":
                            genpass = str(input("Do You want me to Generate A password For You(Y/N): "))

                signup()

            else:
                print("SIGNUP DENIED, Ask for Authorization")
                os.system("pause")
                login(idname=input("Name ID  : "), passw=input("Password : "))


        elif answer == "N" or answer == "n":
            login(idname=input("Name ID  : "), passw=input("Password : "))


        else:
            print("Input a valid OPTION")
            answer = str(input("Press Y/N =  "))
            if answer.lower() == "y":
                key = int(input("Enter Signup Authourization Key =  "))
                if key == passkey:
                    print("Welcome to SIGNUP")
                    #signup()
            
login()