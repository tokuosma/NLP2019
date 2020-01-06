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
import pandas as pd


def analyse_users(users_source_files):
    """
    users_source_files is a list of the json files that contain the user's data in strings
    """
    for source_file in users_source_files:
        
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
            sentiments .append(testimonial.sentiment.polarity)
            # print(text+'   '+str(testimonial.sentiment))
            if testimonial.sentiment.polarity < 0:
                no_neg_posts += 1
                if current_date < lowest_date:
                    lowest_date = current_date
                if current_date > highest_date:
                    highest_date = current_date

        sentiment_mean = mean(sentiments)
        sentiment_stdev =stdev(sentiments)
        # print(sentiment_mean, sentiment_stdev)

        # print(sentiment_stdev)

        for tweet,sentiment in tweets_and_sentiments:
            standardized_value = (sentiment-sentiment_mean)/sentiment_stdev
            # print(standardized_value)
            if standardized_value < -3: # if a negative sentiment is further than 3 standard deviations away from the mean, the post related to it is "very negative"
                very_neg_tweets_and_sentiments.append((tweet, sentiment))
                no_very_neg_posts += 1
            
        time_active = highest_date - lowest_date
        mean_sentiment_perc = (sentiment_mean + 1)* (1/2) # sentiment is between [-1,1]. [-1,1] -> [0,1]
        vol_neg_posts = no_neg_posts/len(tweets)
        vol_very_neg_posts = no_very_neg_posts/len(tweets)
        radicalization_score = (7/mean_sentiment_perc**3)*vol_neg_posts*vol_very_neg_posts*float(time_active.days)

        # print(sentiments)
        # df = pd.DataFrame(sentiments, columns = ['sentiment'])
        # df.hist(bins=50)
        # print('file: ' + source_file)
        # print('mean sentiment percentile: ' + str(mean_sentiment_perc))
        # print('number of negative posts: ' + str(no_neg_posts))
        # print('volume of negative posts: ' + str(vol_neg_posts))
        # print('number of very negative posts:' + str(no_very_neg_posts))
        # print('volume of very negative posts:' + str(vol_very_neg_posts))
        # print('number of days active: '+ str(time_active.days))
        # print('radicalization score: '+ str(radicalization_score))
        # print('very negative post and their sentiments:')
        # [print(str(item[0]),item[1]) for item in very_neg_tweets_and_sentiments]
        # print('\n\n\n')
        return source_file, mean_sentiment_perc, vol_neg_posts, vol_very_neg_posts, time_active.days, radicalization_score, very_neg_tweets_and_sentiments, sentiments

source_files = ['Data\\tweets_user_ViidarUkonpoika.json', 'Data\\tweets_user_UKInfidel.json', 'Data\\tweets_user_DrDavidDuke.json']#, 'Data\\tweets_extremist.json', 'Data\\tweets_bombing.json', 'Data\\tweets_islamophobia.json', 'Data\\tweets_radicalist.json']
thing = analyse_users(source_files)
print(thing)
