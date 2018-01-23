import sqlite3 #enables control of an sqlite database

#------------------------------------------------------
db_name = "data/chillDB.db"

#Run to create the table
def create_table():
    db = sqlite3.connect(db_name)
    c = db.cursor()
    c.execute("CREATE TABLE drawings (id INTEGER PRIMARY KEY, username TEXT, word TEXT, image TEXT, solved INTEGER);")
    db.commit()
    db.close()

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
    
#returns list of dictionaries containing images drawn by a specified user
def get_images_by(username):
    #list_id = [1, 2, 3, 4]
    #list_drawings = []
    #for id in list_id:
    #    list_drawings.append(get_image(id))
    #return list_drawings
    db = sqlite3.connect(db_name)
    c = db.cursor()
    result = c.execute("SELECT image FROM drawings WHERE username = '%s';")%(username)
    print result
    
#returns a list of dictionaries contiaining images that a specified user has guessed
def get_guessed_images(username):
    list_id = [1, 2, 3, 4]
    list_drawings = []
    for id in list_id:
        list_drawings.append(get_image(id))
    return list_drawings

#returns a list of images that a user has drawn.
def get_images_of(word):
    list_id = [1, 2, 3, 4]
    list_drawings = []
    for id in list_id:
        list_drawings.append(get_image(id))
    return list_drawings

#Given a tuple/list and a list of strings, will create a dictionary where the first key in the list corresponds to the first element in the tuple
def tuple_to_dictionary(tuuple, list_of_keys):
    d = {} #the dictionary
    index = 0 #the column index
    while index < len(tuuple):
        d[ list_of_keys[index] ] = tuuple[index]
        index += 1
    return d
