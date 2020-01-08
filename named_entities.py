from util import read_tweets, get_tweet_text, clean_tweet_text
import spacy

ENTITY_HATE = "hate_speech"
ENTITY_NON_HATE = "non_hate_speech"
nlp = spacy.load("en_core_web_sm")

def get_named_entities(tweets):
    results = {
        ENTITY_HATE : {},
        ENTITY_NON_HATE : {}
    }

    num_hate, num_non_hate = 0,0

    for tweet in tweets:
        category = ""
        text = clean_tweet_text(get_tweet_text(tweet))

        if tweet["hate_speech"]:
            category = ENTITY_HATE
            num_hate += 1
        else:
            category = ENTITY_NON_HATE
            num_non_hate += 1
        doc = nlp(text)
        for ent in doc.ents:
            if ent.text == "#":
                break
            if ent.text in results[category]:
                #Way to increase the counter
                results[category][ent.text] += 1
            else:
                results[category][ent.text] = 1

    results[ENTITY_HATE] = sorted(results[ENTITY_HATE].items(), key= lambda kv : (kv[1], kv[0]), reverse=True)
    results[ENTITY_NON_HATE] = sorted(results[ENTITY_NON_HATE].items(), key= lambda kv : (kv[1], kv[0]), reverse=True)

    results[ENTITY_HATE] = [(x, y / num_hate) for x,y in results[ENTITY_HATE]]
    results[ENTITY_NON_HATE] = [(x, y / num_non_hate) for x,y in results[ENTITY_NON_HATE]]

    return results

if __name__ == "__main__":

    f = []
    f.append(input("Give file: "))
    tweets = read_tweets(f)
    results = get_named_entities(tweets)
    
    print("Top 20 entities in hate tweets:")
    for i in range(20):
        print(results[ENTITY_HATE][i][0]+ ": " + str(round(results[ENTITY_HATE][i][1],4)))
    print("\n")
    print("Top 20 entities in non hate tweets:")
    for i in range(20):
        print(results[ENTITY_NON_HATE][i][0]+ ": " + str(round(results[ENTITY_NON_HATE][i][1],4)))