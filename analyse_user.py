import json
import argparse
import re
from textblob import TextBlob
from statistics import mean
from statistics import stdev
from datetime import MAXYEAR
from datetime import MINYEAR
from datetime import datetime
from datetime import date
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# import pandas as pd


def analyse_users(source_file):
    """
    users_source_files is a list of the json files that contain the user's data in strings
    """
        
    tweets_and_sentiments = []
    sentiments = []
    very_neg_tweets_and_sentiments = []
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
        text = re.sub(r'https?:\/\/.*[a-zA-Z0-9.\/_%…]*', '', text, flags=re.MULTILINE)
        text = re.sub(r'@[a-zA-Z0-9.\/_%…]*', '', text, flags=re.MULTILINE)
        testimonial = TextBlob(text)
        current_date = datetime.strptime(tweet['created_at'], "%a %b %d %X %z %Y").date()
        tweets_and_sentiments.append((text, testimonial.sentiment.polarity))
        sentiments.append(testimonial.sentiment.polarity)
        if testimonial.sentiment.polarity < 0:
            no_neg_posts += 1
            if current_date < lowest_date:
                lowest_date = current_date
            if current_date > highest_date:
                highest_date = current_date

    sentiment_mean = mean(sentiments)
    sentiment_stdev = stdev(sentiments)

    for tweet,sentiment in tweets_and_sentiments:
        standardized_value = (sentiment-sentiment_mean)/sentiment_stdev
        # print(tweet, sentiment, standardized_value)
        if standardized_value < -3: # if a negative sentiments standard value is less than -3, the post related to it is "very negative"
            very_neg_tweets_and_sentiments.append((tweet, sentiment))
            no_very_neg_posts += 1
        
    time_active = highest_date - lowest_date
    mean_sentiment_perc = (sentiment_mean + 1)* (1/2) # sentiment is between [-1,1]. [-1,1] -> [0,1]
    vol_neg_posts = no_neg_posts/len(tweets)
    vol_very_neg_posts = no_very_neg_posts/len(tweets)
    radicalization_score = (1/mean_sentiment_perc**3)*vol_neg_posts*vol_very_neg_posts*float(time_active.days)

    statistics_dict = {
    "source_file" : source_file,
    "mean_sentiment_perc" : mean_sentiment_perc,
    "vol_neg_posts" : vol_neg_posts,
    "vol_very_neg_posts" : vol_very_neg_posts,
    "days_active" : time_active.days,
    "radicalization_score" : radicalization_score,
    "very_neg_tweets_and_sentiments" : very_neg_tweets_and_sentiments,
    "sentiments" : sentiments
    }
    return statistics_dict
if __name__ == "__main__":

    first_user = analyse_users('Data\\tweets_user_UK_citizen.json')
    second_user = analyse_users('Data\\tweets_user_Finnish_citizen.json')
    third_user = analyse_users('Data\\tweets_user_White_supremacist.json')
    
    print('file: ' + first_user["source_file"])
    print('mean sentiment percentile: ' + str(first_user["mean_sentiment_perc"]))
    print('volume of negative posts: ' + str(first_user["vol_neg_posts"]))
    print('volume of very negative posts:' + str(first_user["vol_very_neg_posts"]))
    print('number of days active: '+ str(first_user["days_active"]))
    print('radicalization score: '+ str(first_user["radicalization_score"]))
    print('\n\n')
    # print('very negative post and their sentiments:')
    # [print(str(item[0]),item[1]) for item in first_user["very_neg_tweets_and_sentiments"]]


    print('file: ' + second_user["source_file"])
    print('mean sentiment percentile: ' + str(second_user["mean_sentiment_perc"]))
    print('volume of negative posts: ' + str(second_user["vol_neg_posts"]))
    print('volume of very negative posts:' + str(second_user["vol_very_neg_posts"]))
    print('number of days active: '+ str(second_user["days_active"]))
    print('radicalization score: '+ str(second_user["radicalization_score"]))
    print('\n\n')
    # print('very negative post and their sentiments:')
    # [print(str(item[0]),item[1]) for item in second_user["very_neg_tweets_and_sentiments"]]


    print('file: ' + third_user["source_file"])
    print('mean sentiment percentile: ' + str(third_user["mean_sentiment_perc"]))
    print('volume of negative posts: ' + str(third_user["vol_neg_posts"]))
    print('volume of very negative posts:' + str(third_user["vol_very_neg_posts"]))
    print('number of days active: '+ str(third_user["days_active"]))
    print('radicalization score: '+ str(third_user["radicalization_score"]))
    print('\n\n')
    # print('very negative post and their sentiments:')
    # [print(str(item[0]),item[1]) for item in third_user["very_neg_tweets_and_sentiments"]]
