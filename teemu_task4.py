from textblob import TextBlob
from util import read_tweets, get_tweet_text, clean_tweet_text
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import numpy as np
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
    
    textblob_results = textblob_tweets_polarity(tweets)
    print("Textblob results are:")
    print("The Percentage of negative hate:",textblob_results[0])
    print("The percentage of neutral hate is:",textblob_results[1])
    print("The percentage of positive hate is:",textblob_results[2])
    print("The percentage of negative non hate is:",textblob_results[3])
    print("The percentage of neutral non hate is:",textblob_results[4])
    print("The percentage of positive non hate is:",textblob_results[5])
    
    vader_results = vader_tweets_polarity(tweets)
    print("\nVader results are:")
    print("The Percentage of negative hate:",vader_results[0])
    print("The percentage of neutral hate is: ",vader_results[1])
    print("The percentage of positive hate is: ",vader_results[2])
    print("The percentage of negative non hate is: ",vader_results[3])
    print("The percentage of neutral non hate is: ",vader_results[4])
    print("The percentage of positive non hate is: ",vader_results[5])

    labels = ["Positive", "Neutral", "Negative"]
    hate_values = [textblob_results[2], textblob_results[1], textblob_results[0]]
    non_hate_values = [textblob_results[5], textblob_results[4], textblob_results[3]]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, hate_values, width, label="hate_values")
    rects2 = ax.bar(x + width/2, non_hate_values, width, label="non_hate_values")

    ax.set_ylabel("%")
    ax.set_title("Textblob results")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend
    plt.show()

    labels = ["Positive", "Neutral", "Negative"]
    hate_values = [vader_results[2], vader_results[1], vader_results[0]]
    non_hate_values = [vader_results[5], vader_results[4], vader_results[3]]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, hate_values, width, label="hate_values")
    rects2 = ax.bar(x + width/2, non_hate_values, width, label="non_hate_values")

    ax.set_ylabel("%")
    ax.set_title("Vader results")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend
    plt.show()

    labels = ["Positive", "Neutral", "Negative"]
    hate_values = [abs(textblob_results[2] - vader_results[2]), abs(textblob_results[1] - vader_results[1]), abs(textblob_results[0] - vader_results[0])]
    non_hate_values = [abs(textblob_results[5] - vader_results[5]), abs(textblob_results[4] - vader_results[4]), abs(textblob_results[3] - vader_results[3])]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, hate_values, width, label="hate_values")
    rects2 = ax.bar(x + width/2, non_hate_values, width, label="non_hate_values")

    ax.set_ylabel("%")
    ax.set_title("Textblob vs Vader")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend
    plt.tight_layout()