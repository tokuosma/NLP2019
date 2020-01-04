import json
import argparse
from util import clean_tweet_text
from textblob import TextBlob
from statistics import mean
from statistics import stdev
from datetime import MAXYEAR
from datetime import MINYEAR
from datetime import datetime
from datetime import date
import pandas as pd

"""
TODO:
- entiment_stdev kaikista sentimenteista
- urlit ja käyttäjänimet pois

"""

source_files = ['Data\\tweets_user_ViidarUkonpoika.json', 'Data\\tweets_user_UKInfidel.json', 'Data\\tweets_user_DrDavidDuke.json']

for source_file in source_files:
    
    sentiments = []
    no_neg_posts = 0
    no_very_neg_posts = 0
    highest_date = date(MINYEAR, 1, 1)
    lowest_date = date(MAXYEAR, 12, 31)

    with open(source_file,'r') as json_file:
        tweets = json.loads(json_file.read())


    for tweet in tweets:
        if(tweet["truncated"]):
            text = tweet['extended_tweet']['full_text']
        else:
            text = tweet['text']
        text = clean_tweet_text(text)
        testimonial = TextBlob(text)
        current_date = datetime.strptime(tweet['created_at'], "%a %b %d %X %z %Y").date()
        sentiments.append(testimonial.sentiment.polarity)
        # print(text+'   '+str(testimonial.sentiment))
        if testimonial.sentiment.polarity < 0:
            no_neg_posts += 1
            if current_date < lowest_date:
                lowest_date = current_date
            if current_date > highest_date:
                highest_date = current_date

    sentiment_stdev = stdev(sentiments)
    # print(sentiment_stdev)


    for sentiment in sentiments:
        if sentiment < -3*sentiment_stdev: # if a negative sentiment is further than 3 standard deviations away from the mean, the post related to it is "very negative"
            no_very_neg_posts += 1
        
    time_active = highest_date - lowest_date
    mean_sentiment_perc = (mean(sentiments) + 1)* (1/2) # sentiment is between [-1,1]. [-1,1] -> [0,1]
    vol_neg_posts = no_neg_posts/len(tweets)
    vol_very_neg_posts = no_very_neg_posts/len(tweets)

    # print(sentiments)
    df = pd.DataFrame(sentiments, columns = ['sentiment'])
    df.hist(bins=50)
    print('file: '+source_file)
    print('mean sentiment percentile: ' + str(mean_sentiment_perc))
    print('number of negative posts: ' + str(no_neg_posts))
    print('volume of negative posts: ' + str(vol_neg_posts))
    print('number of very negative posts:' + str(no_very_neg_posts))
    print('volume of very negative posts:' + str(vol_very_neg_posts))
    print('number of days active: '+ str(time_active.days))
    print('radicalization score: '+ str((7/mean_sentiment_perc**3)*vol_neg_posts*vol_very_neg_posts*float(time_active.days)))
    print('\n\n\n')