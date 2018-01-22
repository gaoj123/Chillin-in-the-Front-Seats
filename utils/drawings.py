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
