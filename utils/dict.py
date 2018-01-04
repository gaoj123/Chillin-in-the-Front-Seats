#install requests from http://docs.python-requests.org/en/master/user/install/#install
import requests
import json
import random

#CHANGE API_KEY AND APP_ID TO "NOT SECURE" BEFORE SENDING TO GITHUB!!
app_id = 'NOT_SECURE'
app_key = 'NOT_SECURE'

#request for domains
url = 'https://od-api.oxforddictionaries.com/api/v1/domains/en'

r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
domain_dict = json.loads(r.text)['results']
#Manualing Removing some domains from the dictionary
removed_domains = ['Alcoholic', 'Amerindian', 'Audio', 'Australian Rules', 'Biblical', 'Buddhism', 'Crime', 'Crystallography', 'First_World_War', 'Gambling', 'Hinduism', 'Islam', 'Judaism', 'Napoleonic_Wars', 'Occult', 'Penal', 'Phonetics', 'Popular_Music', 'Religion', 'Roman_Catholic_Church', 'Second_World_War', 'Sikhism', 'Smoking', 'Theology', 'War_Of_American_Independence', 'Wine', 'English_Civil_War', 'American_Civil_War'] 
for domain in removed_domains:
    domain_dict.pop(domain, None)

#Create list of topics
def createWordList():
    domain_choices = []
    times = 5
    while times >0:
        choose_once = random.choice(domain_dict.keys())
        domain_choices.append(choose_once)
        times = times - 1
    return domain_choices

#returns a list of 5 words of a given domain
#domain must be written as a string
def returnWords(domain):
    url = 'https://od-api.oxforddictionaries.com:443/api/v1/wordlist/en/lexicalCategory=Noun;domains=' + domain

    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
    words_dict = json.loads(r.text)['results']
    times = 5
    word_list = []
    while times > 0:
        result_word = random.choice(words_dict)
        word = result_word['word'].decode('unicode_escape').encode('ascii','ignore')
        word_list.append(word)
        times = times - 1
    return word_list







