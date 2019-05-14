import sqlite3


with sqlite3.connect("C:\PythonJunk\database\data.db") as db:
    cursor = db.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS userslist(
userID INTEGER PRIMARY KEY,
firstname VARCHAR(20) NOT NULL,
lastname VARCHAR(20) NOT NULL,
dateofbirth VARCHAR(20) NOT NULL,
email VARCHAR(40) NOT NULL,
phone VARCHAR(20) NOT NULL,
username VARCHAR(20) NOT NULL,
password VARCHAR(20) NOT NULL);
""")


cursor.execute("""
INSERT INTO userslist(firstname,lastname,dateofbirth,phone,email,username,password)
VALUES("","","","","","","")
""")
db.commit()


cursor.execute("SELECT * FROM userslist")
print(cursor.fetchall())