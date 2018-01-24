## Team Name: Chillin in the Front Seats
Jenny Gao, Kevin Li, William Soe, Max Zlotskiy <br>
Period 9 <br>
## Project Name: Drawnet
Drawnet is a website where users can play a game similar to Pictionary.  Users have two options: guess other users’ drawings or create their own drawings.  To draw, users first choose what they want to draw from a list of nouns.  They are then led to a canvas - program like Paint - where they draw the object they chose and submit that drawing to be guessed by others.  Drawers will receive notifications regarding other people’s guesses of their drawings.  For the drawer, the drawing is scored as follows: 20 - n (where “n” is the number of guessers who guessed the user’s drawing incorrectly); after all, the quicker the drawing is guessed correctly, the better the quality of the user’s drawing. If the guesser guesses a drawing correctly, the guesser gets 5 points. Thus, each user has two overall scores, as a guesser and as a drawer.   <br><br>
[Video](https://www.youtube.com/)

### Run Instructions 
In terminal:
```
$ git clone https://github.com/gaoj123/Chillin-in-the-Front-Seats.git
$ cd Chillin-in-the-Front-Seats
$ python app.py
```
then go to `localhost:5000` in any browser.

### Play Instructions
* Create an account and log in.  
* You'll be able to create drawings.  On the canvas, there is a color picker, fill bucket, dropper, a color replacer, a scale to adjust brush thickness, and an option to recolor the entire canvas. After submitting your drawing, other users will guess your drawing.  You will then get notifications regarding whether they guessed correctly and what their guesses were.  Once your drawing has been solved, it will be marked as solved and will not be guessed by other users.
* Moreover, you can also guess other users' drawings.  The "Guess" page shows several drawings by other users (will say none available if others have not created drawings).  Clicking on a drawing brings you to a page where you can type what you think the object is into a text field.  Upon submission, you will know whether you guessed correctly or not (+5 points to your "Guesser Score" if correct).  
* You can view all drawings in the "Gallery" page.  Clicking each drawing brings you to a page containing only that drawing and info like number of incorrect guesses.
* In addition, you can view all of the drawings (by other users) that you have guessed in the "Guessed Drawings" route.  Clicking each drawing leads to a page containing only that drawing and info like who drew it.
* The notifications page contains all of your notifications (unseen notifications are highlighted).  Clicking on each notification brings you to a new page with info like all the guesses for the associated drawing (and will also mark the notification as read).
* The "Profile" page displays "Artist Score" (score from your drawings), "Guesser Score" (score from guessing other users' drawings), "Best Image" (and score), "Worst Image" (and score).  It also gives you the option to update your profile picture, which you also could have done when creating an account. <br>

### Bug
One word in our word list causes an ascii error (this happens about 1 in 100 times when the user goes on the "Draw" route and chooses an object to draw).  If this happens, please refresh the "Draw" ("Choose Word") page.<br>

### Note
Our system does not allow for synonyms and singular/plural variants of the answer (object chosen to draw).  For example, if the correct answer is "fire", "flame" will be deemed incorrect.  Another example would be "flowers" - "flower" would be incorrect.

### Created Accounts
You can log onto these pre-existing accounts: <br>
Usernames: dw, max, wsoe, jen, kli16<br>
Password: 123 (for all accounts)

| Username           | Password |
|--------------------|----------|
| `dw`               | 123      | 
| `max`              | 123      |
| `wsoe`             | 123      |
| `jen `             | 123      |
| `kli16`            | 123      |
