'''
Created on 12. mars 2014

@author: JohnArne
'''
import sys
import json
from pprint import pprint
import csv
import codecs

def load_to_tsv():
    """
    Loads tweets from site and store as tsv file.
    """
    json_data = open("data/curl_twitterdata.json")
    data = json.load(json_data)
    tweets = [ x["_source"]["published"]+str("\t")+x["_source"]["publisher"]+str("\t")+x["_source"]["leadText"] for x in data["hits"]["hits"] ]
    for tweet in tweets:
        print tweet
    print len(tweets)
    out = csv.writer(open("data/dataset.tsv","w"), delimiter="\n", quoting=csv.QUOTE_MINIMAL)
    out.writerow(tweets)
    json_data.close()

def get_resultsets_text(results):
    """
    Takes a results list and return a list of test strings
    """
    return [unicode(x.created_at) +str("\t")+ unicode(x.user.screen_name) +("\t")+ unicode(x.text).replace("\n", " ") for x in results]

def get_tweets_text(tweets):
    """
    Returns a list of text bodies for the given set of tweets.
    """
    return [unicode(tweet.text) for tweet in tweets]

def append_to_dataset(text):
    """
    Appends text instances to dataset.
    """
#    sys.stdout = codecs.getwriter('utf8')(sys.stdout)
    f = open("dataset.tsv","a")
    for t in text:
        try:
            f.write(t.encode('utf8')+"\n")
            print t.encode('utf8')+"\n"
        except UnicodeEncodeError:
            print "Unicode Encoding Error: ", t.encode('utf8')
        except UnicodeDecodeError:
            print "Unicode Decoding Error: ", t.encode('utf8')
    f.close()
    
def encode_unicode(textfilepath):
    """
    Encodes a text file into utf8.
    """
    f = open(textfilepath, "r")
    text = []
    while f.next():
        text.append(f.readline())
    f.close()
    f = open(textfilepath, "w")
    for line in text:
        try:
            f.write(line.encode('utf8')+"\n")
        except UnicodeEncodeError:
            print "Unicode Encoding Error: ", line.encode('utf8')
        except UnicodeDecodeError:
            print "Unicode Decoding Error: ", line.encode('utf8')
    f.close()