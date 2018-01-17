import sqlite3 #enables control of an sqlite database
import users

#-------------------------------------------------------
db_name = "data/chillDB.db"

#Creates table for the drawings and associated guesses
def create_table():
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute("CREATE TABLE drawings (id INTEGER PRIMARY KEY, artist STRING, word STRING, image STRING, incorrect_users STRING);")
    db.commit()
    db.close()

#returns a dictionary of the incorrect guesses of a drawing
def get_incorrect_users(drawing_id):
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    incorrect_as_tuple = cursor.execute("SELECT incorrect_users FROM drawings WHERE id='%s';" %(drawing_id)).fetchone()
    db.commit()
    db.close()
    return users.tuple_to_dictionary(incorrect_as_tuple, ["user", "guess"])

def get_artist(drawing_id):
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    artist_as_tuple = cursor.execute("SELECT artist FROM drawings WHERE id='%s';"%(drawing_id)).fetchone()
    db.commit()
    db.close()
    return artist_as_tuple[0]
    
def add_new_drawing(drawing_id, artist_name, answer, bit_image):
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute("INSRT INTO drawings VALUES ('%d', '%s', '%s', '%s', Null);"%(drawing_id, artist_name, answer, bit_image))
    db.commit()
    db.close()

def add_incorrect_guess(drawing_id, user, guess):
    db = sqlite3.connect(db_name)
