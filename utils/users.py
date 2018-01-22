import sqlite3 #enables control of an sqlite database

#-------------------------------------------------------------
db_name = "data/chillDB.db"

#Run once, creates the table
def create_table():
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute("CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT, pfp TEXT, guesser_score INTEGER, artist_score INTEGER, best_img_id INTEGER, worst_img_id INTEGER);")
    cursor.execute("CREATE TABLE notifications (recipient TEXT, message TEXT, link TEXT, seen INTEGER, timestamp TEXT);")
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
    if pfp == '':
        pfp = "/static/notfound.png"
    db = sqlite3.connect(db_name)
    c = db.cursor()
    command = "INSERT INTO users (username, password, pfp, best_img_id, worst_img_id, guesser_score, artist_score) VALUES ('%s', '%s', '%s', Null, Null, 0, 0);"%(user, pw, pfp)
    c.execute(command)
    db.commit()
    db.close()

#Returns a dictionary with these keys: username, pfp, best_image, worst_image, guesser_score, artist_score, number_drawings
def get_user_stats(username):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    username = username.replace("'", "''")
    command = "SELECT username, pfp, best_img_id, worst_img_id, guesser_score, artist_score FROM users WHERE username = '%s';" % username
    c.execute(command)
    user_as_tuple = c.fetchone()
    number_drawings = len(c.execute("SELECT id FROM drawings WHERE username = '%s';" % username).fetchall())
    db.close()
    if user_as_tuple != None:
        user_stats = tuple_to_dictionary(user_as_tuple, ["username", "pfp", "best_image", "worst_image", "guesser_score", "artist_score"])
        user_stats["best_image"] = get_image(user_stats["best_image"])
        user_stats["worst_image"] = get_image(user_stats["worst_image"])
        user_stats["number_drawings"] = number_drawings
        return user_stats
    return {}

#Will update the worst and best score in the USERS table. DB must be an sqlite connection (not cursor). Called by add_guess()
def update_scores_for(username, db):
    c = db.cursor()
    username = username.replace("'", "''")
    min_score_id = c.execute("SELECT drawing_id, min(num) FROM (SELECT drawing_id, count(*) num FROM guesses WHERE drawing_id IN (SELECT drawings.id FROM drawings WHERE username = '%s' AND solved = 1) GROUP BY drawing_id);" % username).fetchone()
    max_score_id = c.execute("SELECT drawing_id, max(num) FROM (SELECT drawing_id, count(*) num FROM guesses WHERE drawing_id IN (SELECT drawings.id FROM drawings WHERE username = '%s' AND solved = 1) GROUP BY drawing_id);" % username).fetchone()
    if (min_score_id == None) or (None in min_score_id):
        return
    else: 
        c.execute("UPDATE users SET best_img_id = %d  WHERE username = '%s';" % (min_score_id[0], username))
        if min_score_id != max_score_id: #to prevent using the same image in both categories
            c.execute("UPDATE users SET worst_img_id = %d WHERE username = '%s';" % (max_score_id[0], username))
    db.commit()

#Returns a list of drawings that the specified user hasnt guessed yet.
def random_drawings(username, count):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    list_id = c.execute("SELECT id FROM drawings WHERE username != '%s' AND solved = 0 AND id NOT IN (SELECT drawing_id FROM guesses WHERE username = '%s')" % (username, username)).fetchall()[:count]
    db.close()
    list_drawings = []
    for id in list_id:
        list_drawings.append(get_image(id[0]))
    return list_drawings

#sends a notification to the specified user. <a href="link">message</a> will appear.
def add_notification_for(username, message, link):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    c.execute("INSERT INTO notifications (recipient, message, link, seen, timestamp) VALUES ('%s', '%s', '%s', 0, datetime('now'))" % (username, message, link))
    db.commit()
    db.close()

#Returns a list of all notifications. Most recent ones will be first. Each one is a dictionary with these keys: message, link, seen (boolean), timestamp (string)
def get_notifications_for(username):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    notifications = c.execute("SELECT message, link, seen, timestamp FROM notifications WHERE recipient = '%s' ORDER BY timestamp DESC;" % username).fetchall()
    db.close()
    index = 0
    while index < len(notifications):
        notifications[index] = tuple_to_dictionary(notifications[index], ["message", "link", "seen", "timestamp"])
        notifications[index]["seen"] = (notifications[index]["seen"] == 1)
        index += 1
    return notifications

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
def update_pfp(username, pfp):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    username = username.replace("'", "''")
    command = "UPDATE users SET pfp = '%s' WHERE username = '%s';" %(pfp, username)
    c.execute(command)
    db.commit()
    db.close()

#Returns their score as an artist
def get_ascore(username):
    return get_user_stats(username)["artist_score"]
#Returns their score as a guesser
def get_gscore(username):
    return get_user_stats(username)["guesser_score"]
#Returns the username of who made the drawing
def get_artist(drawing_id):
    return get_image(drawing_id)["artist"]
#Returns the number of incorrect guesses submitted for a drawing
def get_num_guesses(drawing_id):
    image = get_image(drawing_id)
    if image["solved"] == True:
        return len(image["guesses"]) - 1
    return len(image["guesses"])
#Returns the username of whoever solved the drawing. Assumes that the drawing is solved.
def who_guessed_it(drawing_id):
    return get_image(drawing_id)["guesses"][-1]["username"]
#Returns the score for an individual drawing. Assumes that the drawing is solved.
def get_dscore(drawing_id):
    return 21 - len(get_image(drawing_id)["guesses"])
#Returns the answer given a drawing id
def get_answer(drawing_id):
    return get_image(drawing_id)["word"]
#Returns a user's guess for an image, or None if they haven't guessed yet
def get_guess(username, drawing_id):
    for guess in get_image(drawing_id)["guesses"]:
        if guess["username"] == username:
            return guess["guess"]
    return None

#Given a tuple/list and a list of strings, will create a dictionary where the first key in the list corresponds to the first element in the tuple
def tuple_to_dictionary(tuuple, list_of_keys):
    d = {} #the dictionary
    index = 0 #the column index
    while index < len(tuuple):
        d[ list_of_keys[index] ] = tuuple[index]
        index += 1
    return d

