import json
import re
from datetime import datetime
import argparse
import os.path

CREATED_AT_DATE_FORMAT = "%a %b %d %X %z %Y"

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

def print_hashtag_summary(hashtag, tweets):
    """ Prints summary of the labeled tweet data for a given hash tag
        Keyword arguments:
        hashtag -- Tweet hashtag
        tweets -- Tweets related to the hash tag
    """
    hate_tweets = [tweet for tweet in tweets if tweet['hate_speech'] == True]
    non_hate_tweets = [tweet for tweet in tweets if tweet['hate_speech'] == False]
    print('#' + hashtag + 
        ': Number of hate speech = ' + str(len(hate_tweets)) + 
        ', Number of non hate speech = ' + str(len(non_hate_tweets)) +
        ', Total number of tweets = ' +str(len(tweets)))
    tweet_dates = [datetime.strptime(tweet['created_at'], CREATED_AT_DATE_FORMAT).date() for tweet in tweets]
    print('Oldest tweet date: ' + str(min(tweet_dates)))
    print('Newest tweet date: ' + str(max(tweet_dates)))
    print('\n')    



if __name__ == "__main__":
    pass

