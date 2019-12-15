import json
import os
import argparse
from pprint import pprint

parser = argparse.ArgumentParser(description='Load tweet file (json) and ask user to label tweets'  )
parser.add_argument("source_file", type=str, 
                    help='Source file for tweets (json)')

parser.add_argument('output_file', type=str,
                    help='Output file. Note! If output file exists, any previously labeled tweets will be ignored.')
            
args = parser.parse_args()

source_file = vars(args)["source_file"] 
output_file = vars(args)["output_file"]

tweets = []
try:
    with open(source_file, 'r') as json_file:    
        tweets = json.loads(json_file.read())    
except IOError:
    print("Json file not found at '" + source_file +"'"  )

labeled_tweets = {}

if (os.path.isfile(output_file)):
    # Read previousle labeled tweets from output file
    try:
        with open(output_file, 'r') as json_file:    
            previously_labeled = json.loads(json_file.read())
            for tweet in previously_labeled:
                labeled_tweets[tweet["id"]] = tweet
    except IOError:
        print("Could not open output file at '" + output_file +"'"  )
        exit()
    except json.JSONDecodeError:
        print("Could not open parse json file at '" + output_file +"'"  )

done = False
for tweet in tweets:
    if done:
        break
    if tweet["id"] in labeled_tweets:
        #skip labeled tweets
        continue

    if(tweet["truncated"]):
        text = tweet['extended_tweet']['full_text']
    else:
        text = tweet['text']
    printable_tweet = {
        "1_id" :tweet['id'],
        "2_user": tweet['user']['screen_name'],
        "3_created_at" :tweet['created_at'],
        "4_text" : text
        }
    
    while(True):
        pprint(printable_tweet)
        label = input("Is this hate speech? 1=yes, 0=no, q=quit and save results.\n")
        if(label == "0"):
            tweet["hate_speech"] = 0
            labeled_tweets[tweet["id"]] = tweet
            break
        elif(label == "1"):
            tweet["hate_speech"] = 1
            labeled_tweets[tweet["id"]] = tweet
            break
        elif(label == "q"):
            done = True
            break   
    
with open(output_file, 'w+',encoding = 'utf-8', newline='') as output:
    json.dump(list(labeled_tweets.values()), output, indent=4, sort_keys=True)

        


    





