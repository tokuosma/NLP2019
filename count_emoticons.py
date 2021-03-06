import json
import os
import csv
import argparse
import emojis 
import re
import util 

CATEGORY_HATE = "hate_speech"
CATEGORY_NON_HATE = "non_hate_speech"


def count_tweet_emoticons(tweets):
    results = { CATEGORY_HATE : {}, CATEGORY_NON_HATE : {}}
    hate_total = non_hate_total = 0
    for tweet in tweets:
        text = util.get_tweet_text(tweet)
        text_emojis = emojis.get(text)
        if len(text_emojis) == 0:
            # skip tweet if no emojis present
            continue
        category = ""
        if(tweet["hate_speech"]):
            category = CATEGORY_HATE
            hate_total += 1
        else:
            category = CATEGORY_NON_HATE
            non_hate_total += 1            
        for emoji in text_emojis:
            emoji_key = emojis.decode(emoji)
            if emoji_key not in results[category]:
                results[category][emoji_key] = 1
            else:
                results[category][emoji_key] += 1
                
    # Order by    
    results[CATEGORY_HATE] = sorted(results[CATEGORY_HATE].items(), key = lambda kv : ( kv[1], kv[0]), reverse=True)
    results[CATEGORY_NON_HATE] = sorted(results[CATEGORY_NON_HATE].items(), key = lambda kv : ( kv[1], kv[0]), reverse=True)

    results['hate_total'] = hate_total
    results['non_hate_total'] = non_hate_total
    
    return results


                    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Count the emoticons in labeled tweet files (json). Outputs a csv file with emoticon count in both hate and non hate speech tweets')

    parser.add_argument("source_file", type=str, 
                        help='Source file for labeled tweets (json)')

    parser.add_argument('output_file', type=str, nargs='?',
                        help='(optional) Output file (csv). Default value = "emoticon_counts.csv"',
                        default='emoticon_counts.csv')
                
    args = parser.parse_args()

    source_file = vars(args)["source_file"] 
    output_file = vars(args)["output_file"]

    try:
        with open(source_file, 'r') as json_file:    
            tweets = json.loads(json_file.read())    
    except IOError:
        print("Json file not found at '" + source_file +"'"  )
        exit(-1)


    results = count_tweet_emoticons(tweets)

    print(results)
    
    # try:
    #     with open(output_file,'w',encoding = 'utf-8', newline='') as csv_results:
    #         csv_writer = csv.DictWriter(csv_results, delimiter = ';', fieldnames=['emoji_code','num_hate_speech','num_non_hate_speech'])
    #         csv_writer.writeheader()
    #         for result_key in results.keys():
    #             csv_writer.writerow({'emoji_code':result_key , 'num_hate_speech':results[result_key]['hate_speech'], 'num_non_hate_speech':results[result_key]['non_hate_speech']})            
    # except IOError:
    #     print("Could not create result file at '" + output_file +"'"  )



