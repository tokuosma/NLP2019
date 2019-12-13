# Using OAuth1 auth helper
import json
import os
# import requests
# from requests_oauthlib import OAuth1
from searchtweets import ResultStream, gen_rule_payload, load_credentials, collect_results
import argparse

parser = argparse.ArgumentParser(description='Get tweets with tag')
parser.add_argument('hashtag', metavar='hash', type=str,
                    help='hashtag')

parser.add_argument('max_results', metavar='max_results', nargs = '?', type=int,default=10,
                    help='max number of results saved')

args = parser.parse_args()

hashtag = vars(args)["hashtag"] 
max_results = vars(args)["max_results"]

print(vars(args))
creds_30_day_dev = load_credentials(filename="./secrets/secrets.yaml",
                 yaml_key="search_tweets_30_day_dev",
                 env_overwrite=False)

rule = gen_rule_payload("(#" + hashtag + ") lang:en", results_per_call=100) # testing with a sandbox account
print(rule)

tweets = {}
tweets = collect_results(rule,max_results=max_results,result_stream_args=creds_30_day_dev) # change this if you need to

results = []
for tweet in tweets:    
    if ("retweeted_status" in tweet):
        # Skip retweets
        continue    
    else:
        results.append(tweet)

with open('tweets_' + hashtag + '.json', 'w') as json_file:
    json.dump(results, json_file, indent=4, sort_keys=True)




