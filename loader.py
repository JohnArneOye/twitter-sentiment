'''
Created on 12. feb. 2014

@author: JohnArne
'''
#Take JSON object and extract timestamp, username, text body

import json
from pprint import pprint
import csv


def load_to_tsv():
    json_data = open("data/curl_twitterdata.json")
    data = json.load(json_data)
#    pprint(data)
    tweets = [ x["_source"]["published"]+str("\t")+x["_source"]["publisher"]+str("\t")+x["_source"]["leadText"] for x in data["hits"]["hits"] ]
    for tweet in tweets:
        print tweet
    print len(tweets)
    out = csv.writer(open("data/dataset.tsv","w"), delimiter="\n", quoting=csv.QUOTE_MINIMAL)
    out.writerow(tweets)
    json_data.close()
    
if __name__ == '__main__':
    load_to_tsv()