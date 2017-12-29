import sqlite3 #enables control of an sqlite database

#-------------------------------------------------------------
db_name = "data/chillDB.db"

#Run once, creates the table
def create_table():
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute("CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT, pfp TEXT, best INTEGER, best_img TEXT, worst INTEGER, worst_img TEXT);")
    db.commit()
    db.close()

#Given a username and password, will return true if the two correspond, false otherwise
def validate_login(uname, pword):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    username = username.replace("'", "''")
    users = c.execute("SELECT password FROM users WHERE username='%s';" % (uname,)).fetchone()
    db.close()
    if users == None:
        return False
    return users[0] == pword

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
    users = c.execute(command).fetchall()
    db.close()
    return users

#Adds a new record to the users table    
def add_new_user(user, pw, pfp):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "INSERT INTO users VALUES ('%s', '%s', '%s', 0, '', 0, '');"%(user,pw,pfp)
    c.execute(command)
    db.commit()
    db.close()

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

#Updates a user's best/worst score. If this score is between those two values, nothing happens. Score should be an integer 
#Returns 0 if nothing happened, -1 if new worst score, +1 if new best score (worst is lowest and best is highest)
def update_score(username, score):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    username = username.replace("'", "''")
    command = "SELECT worst, best FROM users WHERE username = '%s';" % (username,)
    c.execute(command)
    scores = c.fetchone()
    score = int(score)
    status = 0
    if scores != None:
        if score < scores[0]:
            command = "UPDATE users SET worst = %d WHERE username = '%s';" % (score, username)
            status = -1
        elif score > scores[1]:
            command = "UPDATE users SET best = %d WHERE username = '%s';" % (score, username)
            status = 1
        c.execute(command)
        db.commit()
    db.close()
    return status

#username and image must both be strings
def update_best_img(username, image):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    username = username.replace("'", "''")
    command = "UPDATE users SET best_img = '%s' WHERE username = '%s';" % (image, username)
    c.execute(command)
    db.commit()
    db.close()

#username and image must both be strings
def update_worst_img(username, image):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    username = username.replace("'", "''")
    command = "UPDATE users SET worst_img = '%s' WHERE username = '%s';" % (image, username)
    c.execute(command)
    db.commit()
    db.close()

#Given a tuple/list and a list of strings, will create a dictionary where the first key in the list corresponds to the first element in the tuple
def tuple_to_dictionary(tuuple, list_of_keys):
    d = {} #the dictionary
    index = 0 #the column index
    while index < len(tuuple):
        d[ list_of_keys[index] ] = tuuple[index]
        index += 1
    return d

#Returns a dictionary with these keys: username, pfp, best_score, best_image, worst_score, worst_image
def get_user_stats(username):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    username = username.replace("'", "''")
    command = "SELECT username, pfp, best, best_img, worst, worst_img FROM users WHERE username = '%s';" % username
    c.execute(command)
    user_as_tuple = c.fetchone()
    db.close()
    if user_as_tuple != None:
        return tuple_to_dictionary(user_as_tuple, ["username", "pfp", "best_score", "best_image", "worst_score", "worst_image"])
    return {}
