# Drawnet
Jenny Gao, Kevin Li, William Soe, Max Zlotskiy

Drawnet is a website where users can play a game similar to Pictionary.  Users first choose what they want to draw from a list of nouns (using Oxford Dictionaries API).  They are then led to a program like Paint, where they draw the object they chose and submit that drawing.  Clarifai API is then called to guess what the drawing is.  The score is the confidence level of the Clarifai API.  The higher the score the better. Users have the option to edit the drawing (up to five times) if they want to improve their score or if the API can't guess the word the user chose based on the image drawn.  If the API can’t guess the drawing despite those five tries, the user gets a score of 0.
