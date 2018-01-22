from flask import Flask, flash, render_template, request, session, redirect, url_for
import sqlite3
import utils.users as users
import random

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
        return redirect(url_for("login_page"))

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
@app.route('/account/notifications')
def notifications():
    if loggedIn():
        user=session["username"]
        notis=users.get_notifications_for(user)
        return render_template("notifications.html", notis=notis, loggedin=loggedIn(), username=user)
    else:
        return redirect(url_for("login_page"))
                                   

#This is the gallery page
@app.route('/gallery')
def gallery():
    if loggedIn():
        user=session["username"]
        return render_template("gallery.html", pics=users.get_images_by(user), loggedin=loggedIn(), username=user)
    else:
        return redirect(url_for("login_page"))

#This is the guessed drawings page
@app.route('/guessed')
def guessed():
    if loggedIn():
        user=session["username"]
        return render_template("guessed.html", notis=users.get_guessed_images(user), loggedin=loggedIn(), username=user)
    else:
        return redirect(url_for("login_page"))

#View each individual drawing by other users that you guessed
@app.route('/guessed/view', methods=["POST"])
def viewGuessed():
    if loggedIn():
        user=session["username"]
        id=request.form["id"]
        userGuess=users.get_guess(user, id)
        answ=users.get_answer(id)
        if userGuess.lower()==ans.lower():
            status="You guessed correctly!"
        else:
            status="Sorry, incorrect"
        return render_template("viewGuessed.html", username=user, word=answ, message=status, response=userGuess, loggedin=loggedIn())
    else:
        return redirect(url_for("login_page"))

#User submits drawing
@app.route('/draw/submit', methods=["POST"])
def submitted():
    if loggedIn():
        user=session["username"]
        word=request.form["word"]
        link=request.form["image"]
        users.add_drawing(user, link, word)
        return render_template("submitted.html", username=user, loggedin=loggedIn())
    else:
        return redirect(url_for("login_page"))

#This is the profile page
@app.route('/account/profile')
def profile_route():
    if loggedIn():
        user=session["username"]
        udict = users.get_user_stats(session["username"]);
        if udict["worst_image"]["image"]=="/static/missing.png":
            worstScore1="N/A"
        else:
           worstScore1=users.get_dscore(udict["worst_image"]["id"])
        if udict["best_image"]["image"]=="/static/missing.png":
            bestScore1="N/A"
        else:
            bestScore1=users.get_dscore(udict["best_image"]["id"])
        return render_template("profile.html", pfp=udict["pfp"],username=user, loggedin=loggedIn(), best=udict["best_image"]["image"], worstScore=worstScore1, bestScore=bestScore1, bestId=udict["best_image"]["id"], worstId=udict["worst_image"]["id"], worst=udict["worst_image"]["image"], number=udict["number_drawings"], artistScore=users.get_ascore(user), guesserScore=users.get_gscore(user))
    else:
        return redirect(url_for("login_page"))

#User guesses what others have drawn
@app.route('/guess')
def guess():
    if loggedIn():
        user=session["username"]
        imgList=users.random_drawings(user, 5)
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

#User chooses to update profile pic
@app.route('/update/profile')
def updatePFP():
    if loggedIn():
        return render_template("updatePFP.html", username=session["username"], loggedin=loggedIn())
    else:
        return redirect(url_for("login_page"))

#User updates profile pic
@app.route('/update/profilePic', methods=["POST"])
def updateLink():
    if loggedIn():
        url=request.form["link"]
        user=session["username"]
        users.update_pfp(user, url)
        users.add_notification_for(user, "You changed your profile picture", "/account/profile")
        return redirect(url_for("profile_route"))
    else:
        return redirect(url_for("login_page"))

#User draws on canvas
@app.route('/draw/canvas')
def draw():
    if loggedIn():
        word=request.args["id"];
        return render_template("painting.html", username=session["username"], wordChosen=word, loggedin=loggedIn())
    else:
        return redirect(url_for("login_page"))

#User choice for guessing other user's image
@app.route('/guess/choice', methods=["POST","GET"])
def choice():
    if loggedIn():
        ID=request.args["id"]
        imageLink=users.get_image(ID)["image"]
        return render_template("guessChoice.html", id=ID, link=imageLink, username=session["username"], loggedin=loggedIn())
    else:
        return redirect(url_for("login_page"))

#User sees score for guessing other user's image
@app.route('/guess/score', methods=["POST"])
def score():
    if loggedIn():
        id=request.form["id"];
        user = session["username"]
        guesserResponse=request.form["guess"]
        correct=users.get_image(id)["word"]
        correctOrNot = users.add_guess(user, id, guesserResponse) 
        guesses = users.get_image(id)["guesses"]
        time = ""
        for guess in guesses:
            if guess["username"]==user:
                time=guess["when"]
        if correctOrNot:
            users.add_notification_for(users.get_artist(id),user+" guessed your drawing of \"" + correct + "\" correctly", "/draw/view?id="+id)
        else:
            users.add_notification_for(users.get_artist(id), user+" incorrectly guessed \""+guesserResponse+"\" on your drawing of \"" + correct + "\"", "/draw/view?id="+id)
        return render_template("score.html", accuracy=correctOrNot, username=session["username"], loggedin=loggedIn())
    else:
        return redirect(url_for("login_page"))

#View image individually, provides info like how many people guessed your drawing incorrectly and who guessed it correctly if it has been solved
@app.route('/draw/view', methods=["POST", "GET"])
def view():
    if loggedIn():
        id=request.args["id"]
        user=session["username"]
        if users.get_image(id)["solved"]==True:
            score="Score: "+str(users.get_dscore(id))
            correctGuesser=users.who_guessed_it(id)
            message=correctGuesser+" guessed your drawing correctly"
        else:
            message=""
            score=""
        numIncorrect=users.get_num_guesses(id)
        image = users.get_image(id)
        if image['solved'] == False:
            return render_template("view.html", link=image["image"], word=image["word"], messageShown=message, scoreSolved=score, incorrectGuessesNum=numIncorrect, guesses=image["guesses"], username=user, loggedin=loggedIn())
        else:
            return render_template("viewSolved.html", link=image["image"], word=image["word"], messageShown=message, scoreSolved=score, incorrectGuessesNum=numIncorrect, guesses=image["guesses"], username=user, loggedin=loggedIn())
    else:
        return redirect(url_for("login_page"))

#This is a halfway point. Notification is marked as seen, and then you are redirected to the link associated with it.
@app.route('/notification/view')
def viewNoti():
    if loggedIn():
        time=request.args.get("time", "2018-01-24 10:00:00")
        user=session["username"]
        redir = request.args.get("redir", "/account/notifications")
        users.read_notification(user, time) #marks as seen = True
        return redirect(redir) #send them to wherever the notification link says to
    else:
        return redirect(url_for("login_page"))

@app.route('/admin')
def adminPage():
    action = request.args.get("action", "")
    target = request.args.get("for", "")
    db = sqlite3.connect("data/chillDB.db")
    c = db.cursor()
    if action == "unsolve":
        c.execute("UPDATE drawings SET solved = 0 WHERE id = %s;" % target)
    elif action == "xguesses":
        c.execute("DELETE FROM guesses WHERE drawing_id = %s" % target)
    elif action == "xscore":
        c.execute("UPDATE users SET guesser_score = 0, artist_score = 0 WHERE username = '%s';" % target)
    db.commit()
    db.close()
    return "You tried <u>" + action + "</u> on <u>" + target + "</u>"

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
