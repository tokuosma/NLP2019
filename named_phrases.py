from util import read_tweets, get_tweet_text, clean_tweet_text
import spacy

CATEGORY_HATE = "hate_speech_topics"
CATEGORY_NON_HATE = "non_hate_speech_topics"
nlp = spacy.load("en_core_web_sm")

def get_named_phrases(tweets):
    results = {
        CATEGORY_HATE : [],
        CATEGORY_NON_HATE : []
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
                pass
            else:
                results[category].append(ent.text)

    return results

if __name__ == "__main__":

    f = []
    f.append(input("Give file: "))
    tweets = read_tweets(f)
    results = get_named_phrases(tweets)
    print(results.get(CATEGORY_HATE))
    print(results.get(CATEGORY_NON_HATE))