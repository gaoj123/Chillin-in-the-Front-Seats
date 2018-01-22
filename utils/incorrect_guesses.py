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




