# Using OAuth1 auth helper
import json
import os
import requests
from requests_oauthlib import OAuth1

# read secrets
dirname = os.path.dirname(__file__)
path = os.path.join(dirname, './secrets/secrets.json')
with open(path, 'r') as myfile:
    data=myfile.read()

# parse file
secrets = json.loads(data)

# init oauth helper
oauth = OAuth1(secrets['API_KEY'],
    client_secret=secrets['API_KEY_SECRET'],
    resource_owner_key=secrets['ACCESS_TOKEN'],
    resource_owner_secret=secrets['ACCESS_TOKEN_SECRET'],
    signature_type='auth_header')


url = "https://api.twitter.com/1.1/search/tweets.json"
# set query
querystring = {"q":"#islamophobia"}

# get tweets
response = requests.request("GET", url, params=querystring, auth=oauth)

# save tweets
statuses = json.loads(response.text)
with open('tweets.json', 'w') as json_file:
    json.dump(statuses, json_file, indent=4, sort_keys=True)



