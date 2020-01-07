from util import read_tweets, get_tweet_text, clean_tweet_text
import spacy

CATEGORY_HATE = "hate_speech_topics"
CATEGORY_NON_HATE = "non_hate_speech_topics"
nlp = spacy.load("en_core_web_sm")

def get_named_entities(tweets):
    results = {
        CATEGORY_HATE : {},
        CATEGORY_NON_HATE : {}
    }

    num_hate, num_non_hate = 0,0

    for tweet in tweets:
        category = ""
        text = clean_tweet_text(get_tweet_text(tweet))

        if tweet["hate_speech"]:
            category = CATEGORY_HATE
            num_hate += 1
        else:
            category = CATEGORY_NON_HATE
            num_non_hate += 1
        doc = nlp(text)
        for ent in doc.ents:
            if ent.text in results[category]:
                #Add way to increase the counter
                results[category][ent.text] += 1
            else:
                results[category][ent.text] = 1

    results[CATEGORY_HATE] = sorted(results[CATEGORY_HATE].items(), key= lambda kv : (kv[1], kv[0]), reverse=True)
    results[CATEGORY_NON_HATE] = sorted(results[CATEGORY_NON_HATE].items(), key= lambda kv : (kv[1], kv[0]), reverse=True)

    results[CATEGORY_HATE] = [(x, y / num_hate) for x,y in results[CATEGORY_HATE]]
    results[CATEGORY_NON_HATE] = [(x, y / num_non_hate) for x,y in results[CATEGORY_NON_HATE]]

    return results

if __name__ == "__main__":

    f = []
    f.append(input("Give file: "))
    tweets = read_tweets(f)
    results = get_named_entities(tweets)
    
    print("Top 20 entities in hate tweets:")
    for i in range(20):
        print(results[CATEGORY_HATE][i][0]+ ": " + str(round(results[CATEGORY_HATE][i][1],4)))
    print("\n")
    print("Top 20 entities in non hate tweets:")
    for i in range(20):
        print(results[CATEGORY_NON_HATE][i][0]+ ": " + str(round(results[CATEGORY_NON_HATE][i][1],4)))