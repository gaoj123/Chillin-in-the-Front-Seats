from flask import Flask, flash, render_template, request, session, redirect, url_for
import sqlite3
import utils.users as users
import utils.drawings as draw

#import utils.dict as dict
import random
#import utils.clarifaiCall as clar

app = Flask(__name__)
app.secret_key = "THIS IS NOT SECURE"
wordlist = []
#Returns true or false depending on whether an account is logged in.
def loggedIn():
    return "username" in session


#The home page displays useful information about our website. Accessible regardless of login status.
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

#This is the notification page
#@app.route('/notifications')
#def notifications():

#This is the gallery page
#@app.route('/gallery')
#def gallery():

#This is the guessed drawings page
#@app.route('/guessed')
#def guessed():

#User submits drawing
#@app.route('/draw/submit')
#def submitted():

#This is the profile page
@app.route('/account/profile')
def profile_route():
    if loggedIn():
        udict = users.get_user_stats(session["username"]);
        return render_template("profile.html", pfp=udict["pfp"],username=session["username"], loggedin=loggedIn(), best=udict["best_image"]["image"], worst=udict["worst_image"]["image"], number=udict["number_drawings"])
    else:
        return redirect(url_for("login_page"))

#User guesses what others have drawn
def guess():
    if loggedIn():
        user=session["username"]
        imgList=draw.random_drawings(user)
        return render_template("guess.html", username=user, loggedin=loggedIn(), images=imgList)
    else:
        return redirect(url_for("login_page"))
    
#User chooses word to draw
@app.route('/draw/new')
def chooseWord():
    if loggedIn():
        wordChoices=[];
        while len(wordChoices)<5:
            word=random.choice(wordlist);
            if word not in wordChoices:
                wordChoices.append(word)
        return render_template("chooseWord.html", words=wordChoices, username=session["username"], loggedin=loggedIn())
    else:
        return redirect(url_for("login_page"))

#User chooses word to draw
#@app.route('/draw/new/domain')
#def chooseWord():
    #if loggedIn():
        #domain=request.args["id"];
        #return render_template("chooseWord.html", words=dict.returnWords(domain), username=session["username"], loggedin=loggedIn())
    #else:
        #return redirect(url_for("login_page"))

#User draws on canvas
@app.route('/draw/canvas')
def draw():
    if loggedIn():
        word=request.args["id"];
        return render_template("painting.html", username=session["username"], wordChosen=word, loggedin=loggedIn())
    else:
        return redirect(url_for("login_page"))

#User sees score for current drawing
@app.route('/draw/score', methods=["POST"])
def score():
    if loggedIn():
        img=request.form["image"];
        #scores=clar.get_results_bits(img);
        word = request.form.get("image", "")
        #if(word in scores):
        #    score = scores[word]
        user = session["username"]
        users.add_drawing(user, img, word, 5) #replace 5 with clarifai confidence
        users.update_scores_for(user)
        return render_template("score.html", username=session["username"], confLevel=5, loggedin=loggedIn())
    else:
        return redirect(url_for("login_page"))
#Log out
@app.route('/account/logout')
def logout():
    if loggedIn():
        session.pop('username')
    return redirect(url_for('home'))

if __name__ == "__main__":
    wordfile = open("static/words.txt", "r")
    wordlist = wordfile.read().split("\n")
    wordfile.close()
    app.debug = True
    app.run()
