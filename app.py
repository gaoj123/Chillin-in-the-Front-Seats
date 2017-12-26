from flask import Flask, flash, render_template, request, session, redirect, url_for
import sqlite3
import utils.users as users

app = Flask(__name__)
app.secret_key = "THIS IS NOT SECURE"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method=="POST":
        db = sqlite3.connect("data/ourDB.db") #opens ourDB.db
        c = db.cursor() #opens a cursor object
        #print request.form['user']
        user = request.form['user']
        print user
        command = "SELECT password FROM users WHERE username='%s';"%(user)
        print command
        c.execute(command)
        credentials = c.fetchall()
        print credentials
        db.close()
        print users.validate_login(user, request.form["password"])
        if credentials:
            password = credentials[0][0]
            if request.form['password'] == password:
                session['user'] = request.form['user']
                return redirect(url_for('home'))
            else:
                flash("Sorry, wrong password and/or username")
        else:
            flash("User not found")
            return redirect(url_for('home'))
    else:
        return render_template("form.html")

@app.route('/join')
def join():
    return render_template("form.html")

@app.route('/joinRedirect', methods=['POST','GET'])
def joinRedirect():
    db = sqlite3.connect("data/ourDB.db") #opens ourDB.db
    print users.get_users()
    print [request.form['user']]
    if (request.form['user'],) in users.get_users():
        flash("Username already taken")
    elif request.form['password'] == request.form['passwordConfirm']:
        users.add_new_user(db, request.form['user'], request.form['password'], request.form['name'])
        db.commit()
        db.close()
        session['user'] = request.form['user']
        return redirect(url_for('home'))
    else:
        flash("Passwords do not match")
    db.close()
    return redirect(url_for('join'))   

@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.debug = True
    app.run()
