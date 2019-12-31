import json
from textblob import TextBlob
from statistics import mean
from statistics import stdev
from datetime import MAXYEAR
from datetime import MINYEAR
from datetime import datetime
from datetime import date

with open('Data\\tweets_user_UKInfidel.json','r') as json_file:    
    tweets = json.loads(json_file.read())

sentiments = []
no_neg_posts = 0
no_very_neg_posts = 0
highest_date = date(MINYEAR, 1, 1)
lowest_date = date(MAXYEAR, 12, 31)

for tweet in tweets:
    if(tweet["truncated"]):
        text = tweet['extended_tweet']['full_text']
    else:
        text = tweet['text']
    testimonial = TextBlob(text)
    date = datetime.strptime(tweet['created_at'], "%a %b %d %X %z %Y").date()
    # print(date)
    if date < lowest_date:
        lowest_date = date
    if date > highest_date:
        highest_date = date
    sentiments.append(testimonial.sentiment.polarity)
    if testimonial.sentiment.polarity < 0:
        no_neg_posts += 1

sentiment_stdev = stdev(sentiments)
time_active = highest_date - lowest_date

for sentiment in sentiments:
    if sentiment < -3*sentiment_stdev:
        no_very_neg_posts += 1
    
    

# print(sentiments)
print('mean sentiment: ' + str(mean(sentiments)))
print('number of negative posts: ' + str(no_neg_posts))
print('volume of negative posts: ' + str(no_neg_posts/len(tweets)))
print('number of very negative posts:' + str(no_very_neg_posts))
print('volume of very negative posts:' + str(no_very_neg_posts/len(tweets)))
print('number of days active: '+ str(time_active.days))