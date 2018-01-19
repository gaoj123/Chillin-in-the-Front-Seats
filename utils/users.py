import sqlite3 #enables control of an sqlite database

#-------------------------------------------------------------
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

#Returns a dictionary with these keys: username, pfp, best_image, worst_image
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

#Stores a drawing and its metadata in the database.
def add_drawing(username, encoded_image, word):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    username = username.replace("'", "''")
    c.execute("INSERT INTO drawings (username, image, word, solved) VALUES ('%s', '%s', '%s', 0);" % (username, encoded_image, word))
    db.commit()
    db.close()

#Returns a dictionary with the following keys: image (encoded), word (what it is), guesses (dictionary), artist (user who made it), id and solved (boolean)
def get_image(id):
    if id == None:
        return {"image": "/static/missing.png", "word": "", "score": 0, "artist": "", "id": None}
    id = int(id)
    db = sqlite3.connect(db_name)
    c = db.cursor()
    image_stats = c.execute("SELECT id, username, image, word, guesses, solved FROM drawings WHERE id = %d;" % id).fetchone()
    db.close()
    if image_stats == None:
        return {}
    else:
        image_dict = tuple_to_dictionary(image_stats, ["id", "artist", "image", "word", "guesses", "solved"])
        image_dict["guesses"] = eval(image_dict["guesses"])
        image_dict["solved"] = (image_dict["solved"] == 1)
        return image_dict

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
def update_pfp(username, pfp):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    username = username.replace("'", "''")
    command = "UPDATE users SET pfp = '%s' WHERE username = '%s';" %(pfp, username)
    c.execute(command)
    db.commit()
    db.close()

#Given a word, will return a list of images drawn of that word. Each item will be a dictionary of the form returned by get_image()
#The results will be sorted by score. The first one will have lowest score, and the last will have the highest.
def get_images_of(word):
    word = word.replace("'", "''")
    db = sqlite3.connect(db_name)
    c = db.cursor()
    images = c.execute("SELECT image, word, username, id, guesses, solved FROM drawings WHERE word = '%s' ORDER BY (length(guesses) - length(replace(guesses, ',', '')) + 1) ASC;" % word).fetchall()
    db.close()
    index = 0
    while index < len(images):
        images[index] = tuple_to_dictionary(images[index], ["image", "word", "artist", "id", "guesses", "solved"])
        images[index]["guesses"] = eval(images[index]["guesses"])
        images[index]["solved"] = (images[index]["solved"] == 1)
        index += 1
    return images

#returns a list of dictionaries, where each dictionary is in the format of get_image(), and they are sorted by score from worst to best
#All the images are by the user you specify.
def get_images_by(username):
    username = username.replace("'", "''")
    db = sqlite3.connect(db_name)
    c = db.cursor()
    images = c.execute("SELECT image, word, username, id, guesses, solved FROM drawings WHERE username = '%s' ORDER BY (length(guesses) - length(replace(guesses, ',', '')) + 1) ASC;" % username).fetchall()
    db.close()
    index = 0
    while index < len(images):
        images[index] = tuple_to_dictionary(images[index], ["image", "word", "score", "artist", "id", "guesses", "id"])
        images[index]["guesses"] = eval(images[index]["guesses"])
        images[index]["solved"] = (images[index]["solved"] == 1)
        index += 1
    return images


#Given a tuple/list and a list of strings, will create a dictionary where the first key in the list corresponds to the first element in the tuple
def tuple_to_dictionary(tuuple, list_of_keys):
    d = {} #the dictionary
    index = 0 #the column index
    while index < len(tuuple):
        d[ list_of_keys[index] ] = tuuple[index]
        index += 1
    return d

