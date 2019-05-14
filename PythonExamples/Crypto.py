import time
import os.path
import os
from flask_login.mixins import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask.app import Flask

#**create direactory***#
try:
    os.system('mkdir C:\crypto')
except Exception:
    pass
#********DATABASE******#
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/crypto/cryptopass.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
   
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def __repr__(self):
        return '<User %r>' % (self.username)


def create_newUser():
    print('\nEnter your new login details y\n')
    uname = str(input("New username:  "))
    passw = str(input("New password:  "))
    user = User(username=uname, password=passw)
    db.session.add(user)
    db.session.commit()
    time.sleep(1)
    first_login()
    
def extension(filename):
    i=filename.find('.')
    return filename[i:]

def getfile():
    #open filegetter with python and get file path with os
    filename = str(input('\nplease enter the path to the file : '))
    try:
        reader = open(filename, 'r')
        ext=extension(filename)
        return {'reader':reader, 'ext':ext}
    except Exception:
        print('Invalid file path....Please enter a valid path ')
        getfile()

#*****Functions*****
#create function to read file and encrypt eny line

def encrypt():
    use = str(input('encrypt a file or text?..( enter f or t ) : '))
    mresult = ''
    ext='.txt'
    if use.lower() == 't':
        message = input("\nWhats The Message :   ")
        bmsg = (message[::-1])
        n = 2
        n += 1
        for i in range(0, len(bmsg)):
            result = (chr(ord(bmsg[i]) - n))
            mresult += result
        print("\n", mresult)
        
    elif use.lower() == 'f':
        file = getfile()
        ext=file['ext']
        for line in file['reader']:
            message = line
            bmsg = (message[::-1])
            n = 2
            n += 1
            for i in range(0, len(bmsg)):
                result = (chr(ord(bmsg[i]) - n))
                mresult += result
            mresult += '\n'
    
    else:
        encrypt()

    def save_file(ext):
        answer = input("\nWould you like to save the Encrypted Message? (Y/N) :  ")
        if answer.lower() == 'y':
            save_path = str(input("\npaste the Path you wish to save the file or press ENTER to save at current directory :  "))
            try:
                name = "Cryptocode"
                completeName = os.path.join(save_path, name + ext)
                with open(completeName, 'w') as file:
                    file.write(mresult)
                    file.close()
                print("\nCheck the directory {}\crytocode.txt for your Encrypted Message".format(save_path))
            except Exception:
                print("No Such Directory '{}\ '  ...Try Again".format(save_path))
                save_file()
            time.sleep(1)
        elif answer.lower() == 'n':
            print("Okay (:-) ...")
        else:
            print("\nENTER A VALID ANSWER")
            save_file()

    save_file(ext)


def decrypt():
    use = str(input('decrypt a file or text?..( enter f or t ) : '))
    mresult = ''
    ext='.txt'
    if use.lower() == 't':
        code = input("Enter The Message :   ")
        result = (code[::-1])
        mresult = ''
        n = 2
        n += 1
        for i in range(0, len(code)):
            read = (chr(ord(result[i]) + n))
            mresult += read
        print("\n", mresult)
        
    elif use.lower() == 'f':
        file = getfile()
        ext=file['ext']
        for line in file['reader']:
            code = line
            result = (code[::-1])
            n = 2
            n += 1
            for i in range(0, len(code)):
                read = (chr(ord(result[i]) + n))
                mresult += read
    
    else:
        decrypt()
    
    def save_file(ext):
        answer = input("\nWould you like to save the Decrypted Message? (Y/N) :  ")
        if answer.lower() == 'y':
            save_path = str(input("\npaste the Path you wish to save the file or press ENTER to save at current directory :  "))
            try:
                name = "Cryptoread"
                completeName = os.path.join(save_path, name + ext)
                with open(completeName, 'w') as file:
                    file.write(mresult)
                    file.close()
                print("\nCheck the directory {}\crytocode.txt for your Decrypted Message".format(save_path))
            except Exception:
                print("No Such Directory '{}\ '  ...Try Again".format(save_path))
                save_file()
            time.sleep(1)
        elif answer.lower() == 'n':
            print("Okay (:-) ...")
        else:
            print("\nENTER A VALID ANSWER")
            save_file()

    save_file(ext)


def engine():
    tool = str(input("PRESS E to ENCRYPT or D to DECRYPT :   "))
    if tool.lower() == 'e':
        encrypt()
        print("\nDO YOU WANT TO EXIT...")
        end()

    elif tool.lower() == 'd':
        decrypt()
        print("\nDO YOU WANT TO EXIT...")
        end()

    elif tool.lower() == 'change':
        print("\nEnter your current details\n")
        old_username = str(input("Enter current username:  "))
        old_password = str(input("Enter current username:  "))
        user = User.query.filter(User.username == old_username, User.password == old_password).first()
        if user:
            print("\nEnter your new login details\n")
            uname = str(input("Enter new username:  "))
            passw = str(input("Enter new password:  "))
            new_user = User(username=uname, password=passw)
            db.session.add(new_user)
            db.session.delete(user)
            db.session.commit()
            print('\nTry your new login details\n')
            login()
        else:
            print('\nInvalid user details\n')
            login()

    elif tool.lower() == 'help()':
        print('\nfor help with encryption use help(e)')
        print('for help with decryption use help(d)')
        print('for help with changing login details use help(c)\n')
        engine()

    elif tool.lower() == 'help(e)':
        print('\nfor help with encryption use help(e)')
        print('for help with decryption use help(d)')
        print('for help with changing use help(c)\n')
        engine()

    elif tool.lower() == 'help(d)':
        print('\nfor help with encryption use help(e)')
        print('for help with decryption use help(d)')
        print('for help with change use help(c)\n')
        engine()

    elif tool.lower() == 'help(c)':
        print('\nfor help with encryption use help(e)')
        print('for help with decryption use help(d)')
        print('for help with change use help(c)\n')
        engine()

    elif tool.lower() == 'end' or tool.lower() == 'exit':
        end()

    else:
        engine()


def end():
    answer = input("Enter Y to EXIT or N to CONTINUE :   ")
    if answer.lower() == 'y':
        print("\nGoodBye")
        time.sleep(1)
        os.system('cls' if os.name=='nt' else 'clear')
    elif answer.lower() == 'n':
        engine()
    else:
        print("\nENTER A VALID ANSWER!!!...")
        end()


def first_login():
    try:
        db.create_all()
        user = User.query.filter(User.username.like("%{}%".format(''))).first()
        if user:
            try:
                print('\nConfirm login details\n')
                username = str(input("Enter username:  "))
                password = str(input("Enter password:  "))
                user = User.query.filter(User.username == username, User.password == password).first()
                if user:
                    print('\n\n')
                    print("\nALERT!!! ALERT!!! ALERT!!!....This is a ONE TIME MESSAGE ")
                    print("when you see the prompt USE YJE FOLLOWING COMMANDS:   '\n")
                    print('COMMAND              ---     ACTION')
                    print('======================================')
                    print('e                    ---     encrypt')
                    print('d                    ---     decrypt')
                    print('end                  ---     close/exit')
                    print('change               ---     change login details')
                    print('help()               ---     for help and tips.\n')
                    engine()
                else:
                    print('\nInvalid details!, Try again.\n')
                    login()
            except Exception as e:
                print(e)
                login()  
        else:
            create_newUser()
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
    try:
        db.create_all()
        user = User.query.filter(User.username.like("%{}%".format(''))).first()
        if user:
            try:
                username = str(input("Enter username:  "))
                password = str(input("Enter password:  "))
                user = User.query.filter(User.username == username, User.password == password).first()
                if user:
                    print('\n\nWelcome\n')
                    engine()
                else:
                    print('\nInvalid Username or Password\n')
                    login()
            except Exception as e:
                print(e)
                login()  
        else:
            create_newUser()
    except Exception as e:
        print(e)
        login()        


login()
