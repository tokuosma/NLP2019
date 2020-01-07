from empath import Empath
from util import read_tweets, get_tweet_text, clean_tweet_text
import argparse

CATEGORY_HATE = "hate_speech"
CATEGORY_NON_HATE = "non_hate_speech"



def analyze_tweets_liwc(tweets):
    """ Uses the Empath library to gather topics found in labeled tweet data
        Keyword arguments:
        tweets -- list of labeled tweet objects
    """
    lexicon = Empath()

    
    results = {
        CATEGORY_HATE : {},
        CATEGORY_NON_HATE : {}
    }

    num_hate = num_non_hate = 0
    
    for tweet in tweets:
        category = ""
        text = clean_tweet_text(get_tweet_text(tweet))

        if(tweet["hate_speech"]):
            category = CATEGORY_HATE
            num_hate += 1
        else:
            category = CATEGORY_NON_HATE
            num_non_hate += 1
        topics = lexicon.analyze(text, normalize=False)    
        for topic in topics.keys():
            if topics[topic] > 0:
                if topic in results[category]:
                    results[category][topic] += topics[topic]
                else:
                    results[category][topic] = topics[topic]

    # Sort the topics by total raw counts
    results[CATEGORY_HATE] = sorted(results[CATEGORY_HATE].items(), key= lambda kv : (kv[1], kv[0]), reverse=True)
    results[CATEGORY_NON_HATE] = sorted(results[CATEGORY_NON_HATE].items(), key= lambda kv : (kv[1], kv[0]), reverse=True)

    # Normalize topic counts by dividing by the total number of tweets in each category
    results[CATEGORY_HATE] = [(x, y / num_hate) for x,y in results[CATEGORY_HATE]]
    results[CATEGORY_NON_HATE] = [(x, y / num_non_hate) for x,y in results[CATEGORY_NON_HATE]]   
    
    return results


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Load tweet file (json)'  )
    parser.add_argument("source_files", type=str, nargs='*',
                    help='Source files for tweets (json)')
    args = parser.parse_args()
    source_files = vars(args)["source_files"] 
    tweets = read_tweets(source_files)
    results = analyze_tweets_liwc(tweets)
    print("Top 20 topics in hate tweets:")
    for i in range(20):
        print(results[CATEGORY_HATE][i][0]+ ": " + str(round(results[CATEGORY_HATE][i][1],4)))
    print("\n")
    print("Top 20 topics in non hate tweets:")
    for i in range(20):
        print(results[CATEGORY_NON_HATE][i][0]+ ": " + str(round(results[CATEGORY_NON_HATE][i][1],4)))

