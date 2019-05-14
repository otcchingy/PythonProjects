import time
import os.path
from sqlalchemy import create_engine
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative.api import declarative_base


#********DATABASE******#
engine = create_engine('sqlite:///C:/PythonJunk/cryptopass.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(12))

    def __repr__(self):
        return "<User(name='%s', password='%s')>" % (self.username, self.password)


def create_database():
    with open('C:/PythonJunk/cryptopass.db','w') as file:
        file.close()
    user = User(username='root', password='root')
    db.session.add(user)
    db.session.commit()
    time.sleep(1)
    first_login()
    


#*****Functions*****


def encrypt():
    message = input("Whats The Message :   ")
    bmsg = (message[::-1])
    n = 2
    mresult = ''
    n += 1
    for i in range(0, len(bmsg)):
        result = (chr(ord(bmsg[i]) - n))
        mresult += result
    print("\n", mresult)

    def save_file():
        answer = input("\nWould you like to save the Encrypted Message? (Y/N) :  ")
        if answer == 'Y' or answer == 'y':
            save_path = str(input("\npaste the Path you wish to save the file or press ENTER to save at current directory :  "))
            try:
                name = str("Crpytocode")
                completeName = os.path.join(save_path, name + ".txt")
                with open(completeName, 'w') as file:
                    file.write(mresult)
                    file.close()
                print("\nCheck the directory {}\crytocode.txt for your Encrypted Message".format(save_path))
            except Exception:
                print("No Such Directory '{}\ '  ...Try Again".format(save_path))
                save_file()
            time.sleep(1)
        elif answer == 'N' or answer == 'n':
            print("Okay (:-) ...")
        else:
            print("\nENTER A VALID ANSWER")
            save_file()

    save_file()


def decrypt():
    code = input("Enter The Message :   ")
    result = (code[::-1])
    mresult = ''
    n = 2
    n += 1
    for i in range(0, len(code)):
        read = (chr(ord(result[i]) + n))
        mresult += read
    print("\n", mresult)

    def save_file():
        answer = input("\nWould you like to save the Decrypted Message? (Y/N) :  ")
        if answer == 'Y' or answer == 'y':
            save_path = str(input("\npaste the Path you wish to save the file or press ENTER to save at current directory :  "))
            try:
                name = str("Crpytoread")
                completeName = os.path.join(save_path, name + ".txt")
                with open(completeName, 'w') as file:
                    file.write(mresult)
                    file.close()
                print("\nCheck the directory {}\crytocode.txt for your Decrypted Message".format(save_path))
            except Exception:
                print("No Such Directory '{}\ '  ...Try Again".format(save_path))
                save_file()
            time.sleep(1)
        elif answer == 'N' or answer == 'n':
            print("Okay (:-) ...")
        else:
            print("\nENTER A VALID ANSWER")
            save_file()

    save_file()


def engine():
    tool = str(input("PRESS E to ENCRYPT or D to DECRYPT :   "))
    if tool == 'e' or tool == 'E':
        encrypt()
        print("\nDO YOU WANT TO EXIT...")
        end()

    elif tool == 'change' or tool == 'Change' or tool == 'CHANGE':
        print("\nEntering User Details\n")
        old_username = str(input("Enter current username:  "))
        old_password = str(input("Enter current username:  "))
        user = session.query(User).filter(username == old_username, password == old_password).first()
        if user:
            print("\nEntering New User Details")
            uname = str(input("Enter new username:  "))
            passw = str(input("Enter new password:  "))
            new_user = User(username=uname, password=passw)
            session.add(new_user)
            session.delete(user)
            session.commit()

        else:
            print('invalid user details')
            login()

    elif tool == 'd' or tool == 'D':
        decrypt()
        print("\nDO YOU WANT TO EXIT...")
        end()

    else:
        engine()


def end():
    answer = input("Enter Y to EXIT or N to CONTINUE :   ")
    if answer == 'Y' or answer == 'y':
        print("GoodBye")
        time.sleep(1)
        exit(1)
    elif answer == 'N' or answer == 'n':
        engine()
    else:
        print("\nENTER A VALID ANSWER!!!...")
        end()


def first_login():
    try:
        Base.metadata.create_all(engine)
        user = session.query(User).filter(username='root', password='root')
        if user:
            try:
                username = str(input("Enter username:  "))
                password = str(input("Enter password:  "))
                user = session.query(User).filter(username == username, password == password).first()
                if user:
                    print(value, ___, end, n, file, sys_stdout, flush, False)
                    engine()
                else:
                    login()
            except Exception as e:
                print(e)
                login()  
        else:
            create_database()
    except Exception as e:
        print(e)
        first_login()

#********STARTING PROGRAM*********


print("                     Welcome To CRYPTO 1.0\n")


print("#####  #####   ##    ##  #####   ######  ######  ############### ")
print("##     ##  ##   ##  ##   ##  ##    ##    ##   #  ##CREATED BY:## ")
print("##     ####       ##     #####     ##    ##   #  ## .CHINGY.  ## ")
print("##     ##  #      ##     ##        ##    ##   #  ## @TECHUP@  ## ")
print("#####  ##   #     ##     ##        ##    ######  ############### \n\n")

#*************LOGIN*************#

def login(): 
    #try:
    Base.metadata.create_all(engine)
    user = session.query(User).filter(username='root', password='root')
    if user:
        try:
            username = str(input("Enter username:  "))
            password = str(input("Enter password:  "))
            user = session.query(User).filter(username == username, password == password).first()
            if user:
                engine()
            else:
                login()
        except Exception as e:
            print(e)
            #login()  
    else:
        create_database()
    #except Exception as e:
        #print(e)
        #login()        


login()