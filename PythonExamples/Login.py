import sqlite3
import time

def login():
    while True:
        username = input("Username:   ")
        password = input("Password:   ")
        with sqlite3.connect("data.db") as db:
            cursor = db.cursor()

        find_user = ("SELECT * FROM users WHERE username = ? AND password = ?")
        cursor.execute(find_user,[(username),(password)])
        results = cursor.fetchall()




        if results:
            for i in results:
                print('Welcome')
                return("exit")
            break


        else:
            print("Invalid Login Details")
            again = input("D you want to try again(y/n):  ")
            if again.lower() == "n":
                print("Goodbye")
                time.sleep(2)


login()