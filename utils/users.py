import sqlite3 #enables control of an sqlite database

#-------------------------------------------------------------
db_name = "data/chillDB.db"

#Run once, creates the table
def create_table():
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute("CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT, pfp TEXT, best_score INTEGER, best_img TEXT, best_word TEXT, worst_score INTEGER, worst_img TEXT, worst_word TEXT);")
    cursor.execute("CREATE TABLE drawings (id INTEGER PRIMARY KEY, username TEXT, word TEXT, image TEXT, score INTEGER);")
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

#Returns True if a username is registered, False otherwise
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

#Adds a new record to the users table. Expects username, password, and a link to their pfp
def add_new_user(user, pw, pfp):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "INSERT INTO users VALUES ('%s', '%s', '%s', Null, Null, Null, Null, Null, Null);"%(user,pw,pfp)
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
def update_score(username, score, image, word):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    username = username.replace("'", "''")
    command = "SELECT worst_score, best_score FROM users WHERE username = '%s';" % (username,)
    c.execute(command)
    scores = c.fetchone()
    score = int(score)
    status = 0
    if scores == None or len(scores) < 2 or scores[0] == None:
        scores = [+1 * 10**6, -1 * 10**6] #unrealistic values so you are guaranteed to pass one of the tests
    if score < scores[0]:
        c.execute("UPDATE users SET worst_score = %d WHERE username = '%s';" % (score, username))
        c.execute("UPDATE users SET worst_img = '%s' WHERE username = '%s';" % (image, username))
        c.execute("UPDATE users SET worst_word = '%s' WHERE username = '%s';" % (word, username))
        status = -1
    elif score > scores[1]:
        c.execute("UPDATE users SET best_score = %d WHERE username = '%s';" % (score, username))
        c.execute("UPDATE users SET best_img = '%s' WHERE username = '%s';" % (image, username))
        c.execute("UPDATE users SET best_word = '%s' WHERE username = '%s';" % (word, username))
        status = 1
    db.commit()
    db.close()
    return status

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
    command = "SELECT username, pfp, best_score, best_img, best_word, worst_score, worst_img, worst_word FROM users WHERE username = '%s';" % username
    c.execute(command)
    user_as_tuple = c.fetchone()
    db.close()
    if user_as_tuple != None:
        return tuple_to_dictionary(user_as_tuple, ["username", "pfp", "best_score", "best_image", "best_word", "worst_score", "worst_image", "worst_word"])
    return {}
