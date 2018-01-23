import sqlite3 #enables control of an sqlite database
import drawings as draw

#-------------------------------------------------------------
##############################
## WHO TOUCHA MY DATABASE?? ##
##############################
db_name = "data/chillDB.db"

#Run once, creates the table
def create_table():
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute("CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT, pfp TEXT, guesser_score INTEGER, artist_score INTEGER, best_img_id INTEGER, worst_img_id INTEGER);")
    cursor.execute("CREATE TABLE drawings (id INTEGER PRIMARY KEY, username TEXT, word TEXT, image TEXT, solved INTEGER);")
    cursor.execute("CREATE TABLE notifications (recipient TEXT, message TEXT, link TEXT, seen INTEGER, timestamp TEXT);")
    cursor.execute("CREATE TABLE guesses (username TEXT, drawing_id INTEGER, guess TEXT, timestamp TEXT);")
    db.commit()
    db.close()

##################
## USER METHODS ##
##################

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
        user_stats["best_image"] = draw.get_image(user_stats["best_image"])
        user_stats["worst_image"] = draw.get_image(user_stats["worst_image"])
        user_stats["number_drawings"] = number_drawings
        return user_stats
    return {}

#Will update the worst and best score in the USERS table. DB must be an sqlite connection (not cursor). Called by add_guess()
def update_scores_for(username, db):
    c = db.cursor()
    username = username.replace("'", "''")
    min_score_id = c.execute("SELECT drawing_id, count(*) num FROM guesses WHERE drawing_id IN (SELECT drawings.id FROM drawings WHERE username = '%s' AND solved = 1) GROUP BY drawing_id ORDER BY num ASC,  drawing_id DESC;" % username).fetchone()
    max_score_id = c.execute("SELECT drawing_id, count(*) num FROM guesses WHERE drawing_id IN (SELECT drawings.id FROM drawings WHERE username = '%s' AND solved = 1) GROUP BY drawing_id ORDER BY num DESC, drawing_id DESC;" % username).fetchone()
    print "min id " + str(min_score_id[0]) + " with " + str(min_score_id[1])
    print "max id " + str(max_score_id[0]) + " with " + str(max_score_id[1])
    if (min_score_id == None) or (None in min_score_id):
        print "quitting"
        return
    else: 
        c.execute("UPDATE users SET best_img_id = %d  WHERE username = '%s';" % (min_score_id[0], username))
        if min_score_id != max_score_id: #to prevent using the same image in both categories
            c.execute("UPDATE users SET worst_img_id = %d WHERE username = '%s';" % (max_score_id[0], username))
    db.commit()

#####################
## DRAWING METHODS ##
#####################

#Stores a drawing and its metadata in the database.
def add_drawing(username, encoded_image, word):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    username = username.replace("'", "''")
    c.execute("INSERT INTO drawings (username, image, word, solved) VALUES ('%s', '%s', '%s', 0);" % (username, encoded_image, word))
    db.commit()
    db.close()

#Returns a dictionary with the following keys: image (encoded), word (what it is), artist (user who made it), id, solved (boolean) and guesses (a list of dictionaries; each dictionary has the keys username, guess, when and are sorted from earliest to last)
def get_image(id):
    if id == None:
        return {"image": "/static/missing.png", "word": "", "score": 0, "artist": "", "id": None, "guesses":[]}
    id = int(id)
    db = sqlite3.connect(db_name)
    c = db.cursor()
    image_stats = c.execute("SELECT id, username, image, word, solved FROM drawings WHERE id = %d;" % id).fetchone()
    wrong_guesses = c.execute("SELECT username, guess, timestamp FROM guesses WHERE drawing_id = %d ORDER BY timestamp ASC;" % id).fetchall()
    db.close()
    if image_stats == None:
        return {}
    else:
        image_dict = tuple_to_dictionary(image_stats, ["id", "artist", "image", "word", "solved"])
        image_dict["solved"] = (image_dict["solved"] == 1)
        image_dict["guesses"] = []
        for g in wrong_guesses:
            image_dict["guesses"].append(tuple_to_dictionary(g, ["username", "guess", "when"]))
        return image_dict

#Stores a guess, then returns True or False depending on if it was right. If it was right, points will be awarded accordingly.
def add_guess(username, drawing_id, guess):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    drawing_id = int(drawing_id)
    correct = c.execute("SELECT word FROM drawings WHERE id = %d;" % drawing_id).fetchone()[0]
    was_guess_correct = (guess.lower() == correct.lower())
    c.execute("INSERT INTO guesses VALUES ('%s', %d, '%s', datetime('now'));" % (username, drawing_id, guess))
    if was_guess_correct == True:
        c.execute("UPDATE drawings SET solved = 1 WHERE id = %d;" % drawing_id)
        c.execute("UPDATE users SET guesser_score = guesser_score + 5 WHERE username = '%s';" % username)
        predecessors = c.execute("SELECT count(*) FROM guesses WHERE drawing_id = %d;" % drawing_id).fetchone()
        if predecessors == None or len(predecessors) == 0:
            predecessors = 0
        else:
            predecessors = predecessors[0] - 1 #subtract one to not account for the correct guess
        points = max(0, 20 - predecessors)
        artist = c.execute("SELECT username FROM drawings WHERE id = %d;" % drawing_id).fetchone()[0]
        c.execute("UPDATE users SET artist_score = artist_score + %d WHERE username = '%s';" % (points, artist))
        db.commit()
        update_scores_for(artist, db)
    db.commit()
    db.close()
    return was_guess_correct

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

#Returns a list of the images the user has guessed on, wrong and correct. Each item is a dictionary like get_image()
def get_guessed_images(username):
    list_id = [1, 2, 3, 4]
    list_drawings = []
    for id in list_id:
        list_drawings.append(get_image(id))
    return list_drawings

#Returns a list of the images the user has drawn. Each item is a dictionary in the format of get_image()
def get_images_by(username):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    results = c.execute("SELECT image FROM drawings WHERE username='%s';")%(username).fetchall()
    print results
    
    

#Returns a list of the images with this word as their answer. Each item is a dictionary in the format of get_image()
def get_images_of(word):
    list_id = [1, 2, 3, 4]
    list_drawings = []
    for id in list_id:
        list_drawings.append(get_image(id))
    return list_drawings


###################
## NOTIFICATIONS ##
###################

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

#Sets a notification to seen = True
def read_notification(username, timestamp):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    c.execute("UPDATE notifications SET seen = 1 WHERE recipient = '%s' AND timestamp = '%s';" % (username, timestamp))
    db.commit()
    db.close()

########################
## CONVENIENT METHODS ##
########################

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
    return draw.get_image(drawing_id)["artist"]
#Returns the number of incorrect guesses submitted for a drawing
def get_num_guesses(drawing_id):
    image = draw.get_image(drawing_id)
    if image["solved"] == True:
        return len(image["guesses"]) - 1
    return len(image["guesses"])
#Returns the username of whoever solved the drawing. Assumes that the drawing is solved.
def who_guessed_it(drawing_id):
    return draw.get_image(drawing_id)["guesses"][-1]["username"]
#Returns the score for an individual drawing. Assumes that the drawing is solved.
def get_dscore(drawing_id):
    return 20 - get_num_guesses(drawing_id)
#Returns the answer given a drawing id
def get_answer(drawing_id):
    return draw.get_image(drawing_id)["word"]
#Returns a user's guess for an image, or None if they haven't guessed yet
def get_guess(username, drawing_id):
    for guess in draw.get_image(drawing_id)["guesses"]:
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
