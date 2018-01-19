import sqlite3 #enables control of an sqlite database
import users

#-------------------------------------------------------
db_name = "data/chillDB.db"

#Creates table for incorrect guesses of a drawing
def create_incorrect_table():
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    command = "CREATE TABLE guesses (user TEXT, drawing_id INTEGER, guess TEXT, datetime TEXT);"
    cursor.execute(command)
    db.commit()
    db.close

def get_guesses(drawing_id):
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    guesses_as_tuple = cursor.execute("SELECT user, guess FROM guesses where drawing_id ='%s';"%(drawing_id)).fetchall()
    db.commit()
    db.close()
    return users.tuple_to_dictionary(guesses_as_tuplem ["user", "guess"])

def add_incorrect_guess(drawing_id, user, guess):
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    command = "INSERT INTO guesses VALUES ('%s'. '%d', '%s', datetime('now'));"%(user, drawing_id, guess)
    cursor.execute(command)
    db.commit()
    db.close()




