#IMPORT CLARIFAI LIBRARY USING PIP
#ex. $pip install clarifai
#Use Latest Version of Python 2.7

from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as C1Image
import json
import base64

CLARIFAI_API_KEY = 'e4b9de2b66484695be3f79fed0fa1fd3'

app = ClarifaiApp(api_key = CLARIFAI_API_KEY)

#retrieving model sets from Clarifai
model = app.models.get("general-v1.3")

########################################################

#Following two methods return python dictionaries
#These are deprecated
#predict with Clarifai using a url

def predict_url(url_to_insert):
    response = model.predict_by_url(url=url_to_insert)
    #decoded_response = json.loads(response)
    return response
    
#predict with Clarifai using a local image
#def predict_path(path_to_file):
   # drawing = C1Image(filename = path_to_file)
   # response = model.predict(drawing)
   # decoded_response = json.loads(response)

########################################################

#predict with Clarifai using base64 png
def predict_base64(bits):
    response = model.predict_by_base64(bits)
    return response

########################################################

#Converts base64 encoded image string into a string containing binary data
def decode(encoded_image_as_string):
    return base64.decodestring(encoded_image_as_string)

########################################################



