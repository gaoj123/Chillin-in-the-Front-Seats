import sqlite3 #enables control of an sqlite database

#-------------------------------------------------------------
db_name = "data/chillDB.db"

#Run once, creates the table
def create_table():
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute("CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT, pfp TEXT, best_img_id INTEGER, worst_img_id INTEGER);")
    cursor.execute("CREATE TABLE drawings (id INTEGER PRIMARY KEY, username TEXT, word TEXT, image TEXT, score INTEGER);")
    db.commit()
    db.close()

#Given a username and password, will return true if the two correspond, false otherwise
def validate_login(uname, pword):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    uname = uname.replace("'", "''")
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
    command = "INSERT INTO users VALUES ('%s', '%s', '%s', Null, Null);"%(user, pw, pfp)
    c.execute(command)
    db.commit()
    db.close()

#TODO: make a function that returns image data and use it in this function
#Returns a dictionary with these keys: username, pfp, best_score, best_image, worst_score, worst_image
def get_user_stats(username):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    username = username.replace("'", "''")
    command = "SELECT username, pfp, best_image_id, worst_img_id FROM users WHERE username = '%s';" % username
    c.execute(command)
    user_as_tuple = c.fetchone()
    db.close()
    if user_as_tuple != None:
        return tuple_to_dictionary(user_as_tuple, ["username", "pfp", "best_image", "worst_image"])
    return {}

#Stores a drawing and its metadata in the database. Score must be an integer. Call update_score_for() after this
def add_drawing(username, encoded_image, word, score):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    username = username.replace("'", "''")
    score = int(score)
    c.execute("INSERT INTO drawings (username, image, word, score) VALUES ('%s', '%s', '%s', %d);" % (username, encoded_image, word, score))
    db.commit()
    db.close()

#Will update the worst and best score in the USERS table.
def update_scores_for(username):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    username = username.replace("'", "''")
    min_score_id = c.execute("SELECT id FROM drawings WHERE username = '%s' AND score = (SELECT min(score) FROM drawings);" % username).fetchone()
    max_score_id = c.execute("SELECT id FROM drawings WHERE username = '%s' AND score = (SELECT max(score) FROM drawings);" % username).fetchone()
    if min_score_id != None and min_score_id != max_score_id: #to prevent using the same image in both categories
        c.execute("UPDATE users SET worst_img_id = %d WHERE username = '%s';" % (min_score_id[0], username))
    if max_score_id != None:
        c.execute("UPDATE users SET best_img_id = %d  WHERE username = '%s';" % (max_score_id[0], username))
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

#Updates a user's profile picture to a new one. Both parameters should be strings. 
def update_password(username, pfp):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    username = username.replace("'", "''")
    command = "UPDATE users SET pfp = '%s' WHERE username = '%s';" %(pfp, username)
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

