import json
import argparse
from textblob import TextBlob
from statistics import mean
from statistics import stdev
from datetime import MAXYEAR
from datetime import MINYEAR
from datetime import datetime
from datetime import date

parser = argparse.ArgumentParser(description='Load tweet file (json)'  )
parser.add_argument("source_file", type=str, 
                    help='Source file for tweets (json)')
args = parser.parse_args()
source_file = vars(args)["source_file"] 

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
    testimonial = TextBlob(text)
    date = datetime.strptime(tweet['created_at'], "%a %b %d %X %z %Y").date()
    sentiments.append(testimonial.sentiment.polarity)
    if testimonial.sentiment.polarity < 0:
        no_neg_posts += 1
        if date < lowest_date:
            lowest_date = date
        if date > highest_date:
            highest_date = date

sentiment_stdev = stdev(sentiments)


for sentiment in sentiments:
    if sentiment < -3*sentiment_stdev: # if sentiment is lower than 3 standard deviations away from the mean, it's a "very negative" post
        no_very_neg_posts += 1
    
time_active = highest_date - lowest_date
mean_sentiment_perc = (mean(sentiments) + 1)* (1/2) # sentiment is between [-1,1]. [-1,1] -> [0,1]
vol_neg_posts = no_neg_posts/len(tweets)
vol_very_neg_posts = no_very_neg_posts/len(tweets)

# print(sentiments)
print('mean sentiment percentile: ' + str(mean_sentiment_perc))
print('number of negative posts: ' + str(no_neg_posts))
print('volume of negative posts: ' + str(vol_neg_posts))
print('number of very negative posts:' + str(no_very_neg_posts))
print('volume of very negative posts:' + str(vol_very_neg_posts))
print('number of days active: '+ str(time_active.days))

print('radicalization score: '+ str((7/mean_sentiment_perc**3)*vol_neg_posts*vol_very_neg_posts*float(time_active.days)))