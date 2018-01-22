from flask import Flask, flash, render_template, request, session, redirect, url_for
import sqlite3
import utils.users as users
#import utils.drawings as draw

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
@app.route('/notifications')
def notifications():
    if loggedIn():
        user=session["username"]
        notSeen=[]
        seen=[]
        notis=users.get_notifications_for(user)
        for noti in notis:
            if noti["seen"]==False:
                notSeen.append(noti)
            else:
                seen.append(noti)
        return render_template("notifications.html", seenNoti=seen, unseen=notSeen, loggedin=loggedIn(), username=user)
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
        users.add_guess(user, id, guesserResponse) 
        correct=users.get_image(id)["word"]
        correctOrNot=guesserResponse.lower()==correct.lower()
        guesses=users.get_image(id)["guesses"]
        for guess in guesses:
            if guess["username"]==user:
                time=guess["when"]
        if correctOrNot:
            users.add_notification_for(users.get_artist(id),user+" guessed your drawing correctly on "+time, "/notification/view?id="+id+"&guesser="+user+"&time="+time)
        else:
            users.add_notification_for(users.get_artist(id), user+" incorrectly guessed "+guesserResponse+" on "+time, "/notification/view?id="+id+"&guesser="+user+"&time="+time)
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
        return render_template("view.html", link=users.get_image(id)["image"], word=users.get_image(id)["word"], messageShown=message, scoreSolved=score, incorrectGuessesNum=numIncorrect, username=user, loggedin=loggedIn())    
    else:
        return redirect(url_for("login_page"))

#view notification individually
@app.route('/notification/view', methods=["POST", "GET"])
def viewNoti():
    if loggedIn():
        id=request.args["id"]
        time=request.args["time"]
        guesser=request.args["guesser"]
        user=session["username"]
        if users.get_image(id)["solved"]==True:
            score="Score: "+str(users.get_dscore(id))
        else:
            score=""
        if users.get_guess(guesser,id).lower()==users.get_answer(id).lower():
            message=guesser+" guessed your drawing correctly on "+time
        else:
            message=guesser+" incorrectly guessed "+users.get_guess(guesser,id)+" on "+time
        numIncorrect=users.get_num_guesses(id)
        return render_template("view.html", link=users.get_image(id)["image"], word=users.get_image(id)["word"], messageShown=message, scoreSolved=score, incorrectGuessesNum=numIncorrect, username=user, loggedin=loggedIn())    
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
