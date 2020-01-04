# Using OAuth1 auth helper
import json
import os
# import requests
# from requests_oauthlib import OAuth1
from searchtweets import ResultStream, gen_rule_payload, load_credentials, collect_results
import argparse

parser = argparse.ArgumentParser(description='Get tweets with tag')
parser.add_argument('user', metavar='user', type=str,
                    help='Screen name of the user')

parser.add_argument('max_results', metavar='max_results', nargs = '?', type=int,default=10,
                    help='max number of results saved')

args = parser.parse_args()

user = vars(args)["user"] 
max_results = vars(args)["max_results"]

print(vars(args))
creds_full_archive_dev = load_credentials(filename="./secrets/secrets.yaml",
                 yaml_key="search_tweets_fullarchive_dev",
                 env_overwrite=False)

rule = gen_rule_payload("(from:"+ user + ") lang:en",
    from_date="2015-01-01",
    results_per_call=100) # testing with a sandbox account
print(rule)

tweets = {}
tweets = collect_results(rule,max_results=max_results,result_stream_args=creds_full_archive_dev) # change this if you need to

# OBS! Include retweets for full archive search. 
# Since we are gathering tweets from a single account, no duplicate
# retweets should appear.
# results = []
# for tweet in tweets:    
#     if ("retweeted_status" in tweet):
#         # Skip retweets
#         continue    
#     else:
#         results.append(tweet)

with open('tweets_user_' + user + '.json', 'w') as json_file:
    json.dump(tweets, json_file, indent=4, sort_keys=True)




