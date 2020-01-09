from textblob import TextBlob
from util import read_tweets, get_tweet_text, clean_tweet_text
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import argparse

#Negative (-1 - (-0,33...))
#Neutral (-0,33... - 0,33...)
#Positive (0,33... - 1)

def textblob_tweets_polarity(tweets):
    num_hate = num_non_hate = num_hate_negative = num_hate_neutral = num_hate_positive = num_non_hate_negative = num_non_hate_neutral = num_non_hate_positive = 0
    for tweet in tweets:
        text = clean_tweet_text(get_tweet_text(tweet))
        if(tweet["hate_speech"]):
            num_hate += 1
            polarity = TextBlob(text).polarity
            if(polarity < -0.333):
                num_hate_negative += 1
            elif(polarity < -0.333 or polarity > 0.333):
                num_hate_neutral += 1
            else:
                num_hate_positive += 1
        else:
            num_non_hate += 1
            polarity = TextBlob(text).polarity
            if(polarity < -0.333):
                num_non_hate_negative += 1
            elif(polarity < -0.333 or polarity > 0.333):
                num_non_hate_neutral += 1
            else:
                num_non_hate_positive += 1

    negative_hate = num_hate_negative / num_hate * 100
    neutral_hate = num_hate_neutral / num_hate * 100
    positive_hate = num_hate_positive / num_hate * 100
    
    negative_non_hate = num_non_hate_negative / num_non_hate * 100
    neutral_non_hate = num_non_hate_neutral / num_non_hate * 100
    positive_non_hate = num_non_hate_positive / num_non_hate * 100
    
    return negative_hate, neutral_hate, positive_hate, negative_non_hate, neutral_non_hate, positive_non_hate


def vader_tweets_polarity(tweets):
    trained_num_hate = trained_num_non_hate = trained_num_hate_negative = trained_num_hate_neutral = trained_num_hate_positive = trained_num_non_hate_negative = trained_num_non_hate_neutral = trained_num_non_hate_positive = 0
    for tweet in tweets:
        text = clean_tweet_text(get_tweet_text(tweet))
        if(tweet["hate_speech"]):
            trained_num_hate += 1
            analyser = SentimentIntensityAnalyzer()
            res = analyser.polarity_scores(text)
            polarity = (res["compound"])
            if(polarity < -0.333):
                trained_num_hate_negative += 1
            elif(polarity < -0.333 or polarity > 0.333):
                trained_num_hate_neutral += 1
            else:
                trained_num_hate_positive += 1
        else:
            trained_num_non_hate += 1
            analyser = SentimentIntensityAnalyzer()
            res = analyser.polarity_scores(text)
            polarity = res["compound"]
            if(polarity < -0.333):
                trained_num_non_hate_negative += 1
            elif(polarity < -0.333 or polarity > 0.333):
                trained_num_non_hate_neutral += 1
            else:
                trained_num_non_hate_positive += 1

    trained_negative_hate = trained_num_hate_negative / trained_num_hate * 100
    trained_neutral_hate = trained_num_hate_neutral / trained_num_hate * 100
    trained_positive_hate = trained_num_hate_positive / trained_num_hate * 100
    
    trained_negative_non_hate = trained_num_non_hate_negative / trained_num_non_hate * 100
    trained_neutral_non_hate = trained_num_non_hate_neutral / trained_num_non_hate * 100
    trained_positive_non_hate = trained_num_non_hate_positive / trained_num_non_hate * 100
    

    return trained_negative_hate, trained_neutral_hate, trained_positive_hate, trained_negative_non_hate, trained_neutral_non_hate, trained_positive_non_hate

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Load tweet file (json)'  )
    parser.add_argument("source_files", type=str, nargs='*',
                    help='Source files for tweets (json)')
    args = parser.parse_args()
    source_files = vars(args)["source_files"] 
    tweets = read_tweets(source_files)
    negative_hate, neutral_hate, positive_hate, negative_non_hate, neutral_non_hate, positive_non_hate = textblob_tweets_polarity(tweets)

    print("The next 6 lines are for textblob sentiment analyzer")
    print("The percentage of negative hate is: ",negative_hate)
    print("The percentage of neutral hate is: ",neutral_hate)
    print("The percentage of positive hate is: ",positive_hate)
    print("The percentage of negative non hate is: ",negative_non_hate)
    print("The percentage of neutral non hate is: ",neutral_non_hate)
    print("The percentage of positive non hate is: ",positive_non_hate)

    trained_negative_hate, trained_neutral_hate, trained_positive_hate, trained_negative_non_hate, trained_neutral_non_hate, trained_positive_non_hate = vader_tweets_polarity(tweets)
    
    print("The next 6 lines are for Vader sentiment analyzer")
    print("The percentage of negative hate is: ",trained_negative_hate)
    print("The percentage of neutral hate is: ",trained_neutral_hate)
    print("The percentage of positive hate is: ",trained_positive_hate)
    print("The percentage of negative non hate is: ",trained_negative_non_hate)
    print("The percentage of neutral non hate is: ",trained_neutral_non_hate)
    print("The percentage of positive non hate is: ",trained_positive_non_hate)