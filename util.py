import json
import re
import argparse
import os.path

def read_tweets(paths):
    """ Returns a list of tweet objects obtained from reading all tweet json files specified in paths
        Keyword arguments:
        paths -- list of file paths containing the tweet json files    
    """
    tweets = []
    for path in paths:
        if(os.path.isfile(path)):
            with open(path,'r') as json_file:
                tweets += json.loads(json_file.read())                   
    return tweets

def get_tweet_text(tweet):
    """ Returns the full text from tweet object
        Keyword arguments:
        tweet -- tweet object    
    """
    text = ""
    if(tweet["truncated"]):
        text = tweet['extended_tweet']['full_text']
    else:
        text = tweet['text']
    return text


def clean_tweet_text(text):
    """ Cleans out urls and user names from tweet text
        Keyword arguments:
        text -- tweet text to be cleaned
    """
    text = re.sub(r'https?:\/\/.*[a-zA-Z0-9.\/_%…]*', '', text, flags=re.MULTILINE)
    text = re.sub(r'@[a-zA-Z0-9.\/_%…]*', '', text, flags=re.MULTILINE)
    return text

if __name__ == "__main__":
    pass

