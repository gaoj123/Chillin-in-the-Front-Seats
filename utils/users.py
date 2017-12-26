import sqlite3 #enables control of an sqlite database

#-------------------------------------------------------------
db_name = "data/ourDB.db"

#Run once, creates the table
def create_table():
    cursor.execute("CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT, full_name TEXT, likes TEXT, contributions TEXT);")

def user_exists(username):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "SELECT * FROM users WHERE username = '%s';"%(username)
    result = c.execute(command).fetchone()
    db.commit()
    db.close()
    if result:
        return True 
    else:
        return False

def get_users():
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "SELECT username FROM users;"
    return c.execute(command).fetchall()

#Adds a new record to the users table    
def add_new_user(db, user, pw, name):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "INSERT INTO users VALUES ('%s', '%s', '%s', '', '');"%(user,pw,name)
    c.execute(command)
    db.commit()
    db.close()
    print 'done'

#Updates a user's username to a new one    
def update_username(old_user, new_user):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "UPDATE users SET username = '%s' WHERE username = '%s';" %(new_user,old_user)
    c.execute(command)
    db.commit()
    db.close()

#Updates a user's password to a new one    
def update_password(user, old_pass, new_pass):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "UPDATE users SET password = '%s' WHERE password = '%s' AND username = '%s';" %(new_pass,old_pass,user)
    c.execute(command)
    db.commit()
    db.close()

#Updates a user's fullname to a new one    
def update_fullname(user, new_name):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "UPDATE users SET fullname = '%s' WHERE username = '%s';" % (new_name, user)
    c.execute(command)
    db.commit()
    db.close()
