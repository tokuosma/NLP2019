import json
import csv

with open('./tweets_terrorist.json', 'r') as myfile:
    data=myfile.read()

tweets = json.loads(data)
# print len(tweets)





with open('tweets_terrorist.csv', 'w+',encoding = 'utf-8', newline='') as csv_tweets:
    twitter_writer = csv.DictWriter(csv_tweets, delimiter = ';', fieldnames=['id','user','created at','tweet','label'])
    for tweet in tweets:
        if(tweet["truncated"]):
            text = tweet['extended_tweet']['full_text']
            print(text)
        else:
            text = tweet['text']
        if(tweet["truncated"]):
            text = tweet['extended_tweet']['full_text']
            print(text)
        else:
            text = tweet['text']
            print(text)
        twitter_writer.writerow({'id':tweet['id_str'], 'user':tweet['user']['screen_name'], 'created at':tweet['created_at'], 'tweet':text, 'label':'0'})
        

