import json
import os
import csv
import argparse
import emojis 
import re 


parser = argparse.ArgumentParser(description='Count the emoticons in labeled tweet files (json). Outputs a csv file with emoticon count in both hate and non hate speech tweets')

parser.add_argument("source_file", type=str, 
                    help='Source file for labeled tweets (json)')

parser.add_argument('output_file', type=str, nargs='?',
                    help='Output file. Note! If output file exists, any previously labeled tweets will be ignored.',
                    default='emoticon_counts.csv')
            
args = parser.parse_args()

source_file = vars(args)["source_file"] 
output_file = vars(args)["output_file"]

try:
    with open(source_file, 'r') as json_file:    
        tweets = json.loads(json_file.read())    
except IOError:
    print("Json file not found at '" + source_file +"'"  )

results = {}

for tweet in tweets:
    text = ""
    if(tweet["truncated"]):
        text = tweet['extended_tweet']['full_text']
    else:
        text = tweet['text']
    text_emojis = emojis.get(text)
    for emoji in text_emojis:
        emoji_key = emojis.decode(emoji)
        if emoji_key not in results:
            results[emoji_key] = {'hate_speech' : 0, 'non_hate_speech': 0}
        if tweet['hate_speech'] == True:
                results[emoji_key]['hate_speech'] += 1
        else:
            results[emoji_key]['non_hate_speech'] += 1

try:
    with open(output_file,'w',encoding = 'utf-8', newline='') as csv_results:
        csv_writer = csv.DictWriter(csv_results, delimiter = ';', fieldnames=['emoji_code','num_hate_speech','num_non_hate_speech'])
        csv_writer.writeheader()
        for result_key in results.keys():
            csv_writer.writerow({'emoji_code':result_key , 'num_hate_speech':results[result_key]['hate_speech'], 'num_non_hate_speech':results[result_key]['non_hate_speech']})            
except IOError:
    print("Could not create result file at '" + output_file +"'"  )
                    


            

        




