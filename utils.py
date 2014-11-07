'''
Created on 12. mars 2014

@author: JohnArne
'''
import sys
import os
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

def append_to_dataset(text, dataset):
    """
    Appends text instances to dataset.
    """
#    sys.stdout = codecs.getwriter('utf8')(sys.stdout)
    print "Appending to dataset: "+str(dataset)
    f = open(dataset, "a")
    for t in text:
        try:
            f.write(t.encode('utf8')+"\n")
            print t.encode('utf8')+"\n"
        except UnicodeEncodeError:
            print "Unicode Encoding Error: ", t.encode('utf8')
        except UnicodeDecodeError:
            print "Unicode Decoding Error: ", t.encode('utf8')
    f.close()
    
    
def store_dataset(text, dataset):
    """
    Stores the given sequence of strings to the given dataset as .tsv file.
    """
    print "Storing to dataset: "+str(dataset)
    f = open(dataset, "w")
    for t in text:
#        print unicode("Encoding: ")
#        print unicode(t, 'cp866')
#        encodedline = unicode(t, 'cp866').encode('utf8')
#        print "Writing: "+encodedline
        try:
            f.write(t.encode('utf8'))
        except UnicodeDecodeError:
            f.write(t)
    f.close()
    
def encode_unicode():
    """
    Encodes all text files into utf8.
    """
    f = open("complete_datasets/random_dataset.tsv", "r")
    text = f.readlines()
    f.close()
    f = open("encoding_attempt/random_dataset.tsv", "w")
    for line in text:
        line = line.decode('ascii')
        f.write(line.encode('utf8')+"\n")
    f.close()
    
def select_dataset():
    setnr = raw_input("Write to which dataset? 0: RandomSet 1: ObjectiveSet 2: RoseborgSet 3: ErnaSet ... ")
    return datasets[int(setnr)]

def select_complete_dataset():
    setnr = raw_input("Write to which complete dataset? 0: RandomSet 1: ObjectiveSet 2: RoseborgSet 3: ErnaSet ... ")
    return complete_datasets[int(setnr)]


def get_dataset(dataset):
    """
    Gets the given dataset from file as a list of strings.
    """
    f = open(dataset, "r")
    lines = f.readlines()
    encodedlines = []
    for line in lines:
        encodedlines.append(line)
    f.close()
    return encodedlines
    
    
sentiments = ["negative",
              "neutral",
              "positive"]

complete_datasets = ["complete_datasets/random_dataset.tsv",
                    "complete_datasets/rosenborg_dataset.tsv",
                    "complete_datasets/erna_dataset.tsv"]

datasets = ["data/random_dataset.tsv",
            "data/rosenborg_dataset.tsv",
            "data/erna_dataset.tsv"]    