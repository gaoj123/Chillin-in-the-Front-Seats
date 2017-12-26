from flask import Flask, flash, render_template, request, session, redirect, url_for
import sqlite3
import utils.users as users


app = Flask(__name__)
app.secret_key = "THIS IS NOT SECURE"

def loggedIn():
    return "username" in session

@app.route('/')
def home():
    return render_template('home.html', loggedin=loggedIn())

#This is the page users see. It asks for username and password.
@app.route('/account/login')
def login_page():
    if loggedIn():
        return redirect(url_for("profile_route"))
    else:
        return render_template("login.html")

#This is where the login form leads. On succesful login -> profile page. Otherwise back to /account/login
@app.route('/account/login/post', methods=['POST'])
def login_logic():
    uname = request.form.get("username", "")
    pword = request.form.get("password", "")
    if users.validate_login(uname, pword):
        session["username"] = uname
        return redirect(url_for("profile_route"))
    else:
        flash("Wrong username or password.")
        return redirect(url_for("login_logic"))

#This si the page users see when making an account. Asks for username, password & confirm, and a link to a profile picture.
@app.route('/account/create')
def join():
    if not loggedIn():
        return render_template("join.html")
    else:
        return redirect(url_for("profile_route"))

#This is where the create account form leads. Not done yet.
@app.route('/account/create/post', methods=['POST'])
def joinRedirect():
    uname = request.form.get("username", "")
    pword = request.form.get("password", "")
    pass2 = request.form.get("passwordConfirm", "")
    pfp_url = request.form.get("pfp", "")
    if users.user_exists(uname):
        flash("This account name has already been taken, so please choose another.")
        return redirect(url_for("join"))
    elif pword != pass2:
        flash("Make sure you retype your password the same way in both boxes.")
        return redirect(url_for("join"))
    else:
        users.add_new_user(uname, pword, pfp_url)
        flash('The account "' + uname + '" has been created. Please login to confirm.')
        return redirect(url_for("login_page"))
    """
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
    return redirect(url_for('join'))   """

@app.route('/account/profile')
def profile_route():
    if loggedIn():
        return render_template("profile.html", username=session["username"], loggedin=loggedIn())
    else:
        return redirect(url_for("login_page"))

@app.route('/account/logout')
def logout():
    if loggedIn():
        session.pop('username')
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.debug = True
    app.run()
