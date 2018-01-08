# Drawnet
Jenny Gao, Kevin Li, William Soe, Max Zlotskiy <br>
Period 9

Drawnet is a website where users can play a game similar to Pictionary.  Users first choose what they want to draw from a list of nouns.  They are then led to a program like Paint, where they draw the object they chose and submit that drawing.  Clarifai API is then called to guess what the drawing is.  The score is the confidence level of the Clarifai API.  The higher the score the better. If the API can’t guess the drawing, the user gets a score of 0.
