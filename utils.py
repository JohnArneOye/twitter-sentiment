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
import pickle
import random
import operator

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
    setnr = raw_input("Write to which dataset? 0: RandomSet 1: RoseborgSet 2: ErnaSet ... ")
    return datasets[int(setnr)]

def select_complete_dataset():
    setnr = raw_input("Write to which complete dataset? 0: RandomSet 1: RoseborgSet 2: ErnaSet 3: TemporalSet... ")
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

def store_pickles(tweets, filepath):
    """
    Stores a given list of tweets as pickles.
    """
    output = open("tweet_pickles/"+filepath, 'wb')
    pickle.dump(tweets, output)
    
def get_pickles(setnr=None):
    """
    Gets the stored tweet pickles.
    """
    if setnr==None:
        setnr = int(raw_input("Get which pickle set? 0: RandomSet 1: RoseborgSet 2: ErnaSet 3: All three ..."))
        
    if setnr is 3:
        #fetch all sets and append them together
        tweets = []
        for pickleset in pickles:
            tweets = tweets + pickle.load(open(pickleset, 'rb'))
            print len(tweets)
        return tweets
    else:
        tweets = pickle.load(open(pickles[setnr], 'rb'))
        return tweets
    
    return tweets

def get_all_pickles():
    """
    Gets ALL the stored tweet pickles.
    """
    tweets = []
    for pickleset in pickles:
        tweets = tweets + pickle.load(open(pickleset, 'rb'))
    tweets = tweets + pickle.load(open('temporal_tweets1', 'rb'))
    tweets = tweets + pickle.load(open('temporal_tweets2', 'rb'))
    print len(tweets)
    return tweets
   
def limit_topics_top10(data):
    """
    Takes in a set of plotting data, and limits the topics to top 10 most frequent.
    """
    

def split_train_and_test(tweets):
    """
    Splits the given tweet set into a training set and a testing set.
    """
    split_pos = int(len(tweets)*0.8)
    train_tweets = tweets[0:split_pos]
    test_tweets = tweets[split_pos:len(tweets)]
    return train_tweets, test_tweets

def make_polarity_train_and_test_and_targets(tweets, sentimentvalues, splitvalue=0.9, reduce_dataset=1, shuffle=True):
    """
    Removes objective tweets and returns a completely subjective dataset, along with the positive or negative targets.
    """
    
    pol_tweets = []
    pol_sentiments = []
    if shuffle:
        tweets, sentimentvalues = shuffle_tweets_and_sentiments(tweets, sentimentvalues)
    for t,s in zip(tweets, sentimentvalues):
        if t.subjectivity==1:
            pol_tweets.append(t)
            pol_sentiments.append(s)
    pol_tweets = pol_tweets[:int(round(reduce_dataset*len(pol_tweets)))] 
    pol_sentiments = pol_sentiments[:int(round(reduce_dataset*len(pol_sentiments)))]
    up_to = int(round(len(pol_tweets)*(splitvalue+0.1)))
    split_pos = int(round(len(pol_tweets)*splitvalue))
    train_tweets = pol_tweets[0:split_pos]+pol_tweets[up_to:len(pol_tweets)]
    test_tweets = pol_tweets[split_pos:up_to]
    train_sentimentvalues = pol_sentiments[0:split_pos]+pol_sentiments[up_to:len(pol_tweets)]
    test_sentimentvalues = pol_sentiments[split_pos:up_to]
    
    pol_train_targets = [t.get_sentiment() for t in train_tweets]
    pol_test_targets = [t.get_sentiment() for t in test_tweets]
    print "Train tweets: ", len(train_tweets)
    print "test tweeets: ", len(test_tweets) 
    print "Train targets: ", len(pol_train_targets)
    print "test targets ", len(pol_test_targets)
    print "train sentiments ", len(train_sentimentvalues)
    print "test sentiments ", len(test_sentimentvalues)
    return train_tweets, pol_train_targets, test_tweets, pol_test_targets, train_sentimentvalues, test_sentimentvalues
    
def make_subjectivity_train_and_test_and_targets(tweets, sentimentvalues, splitvalue=0.9, reduce_dataset=1,shuffle=True):
    """
    Returns a dataset for subjectivity classification, along with the targets for classification
    """
    if shuffle:
        tweets, sentimentvalues = shuffle_tweets_and_sentiments(tweets, sentimentvalues)
    reduced_tweets = tweets[:int(round(reduce_dataset*len(tweets)))] 
    up_to = int(round(len(reduced_tweets)*(splitvalue+0.1)))
    split_pos = int(round(len(reduced_tweets)*splitvalue))
    
    print "Upto:",up_to
    print "Splitpos:",split_pos
    train_tweets = reduced_tweets[:split_pos]+reduced_tweets[up_to:len(reduced_tweets)]
    test_tweets = reduced_tweets[split_pos:up_to]
    train_sentimentvalues = sentimentvalues[0:split_pos]+sentimentvalues[up_to:len(reduced_tweets)]
    test_sentimentvalues = sentimentvalues[split_pos:up_to]
    print "Train reduced_tweets: ", len(train_tweets)
    print "test tweeets: ", len(test_tweets) 
    
    sub_train_targets = ['objective' if t.subjectivity==0 else 'subjective' for t in train_tweets]
    sub_test_targets = ['objective' if t.subjectivity==0 else 'subjective' for t in test_tweets]
    print "Train targets: ", len(sub_train_targets)
    print "test targets ", len(sub_test_targets)
    return train_tweets, sub_train_targets, test_tweets, sub_test_targets, train_sentimentvalues, test_sentimentvalues


def shuffle_tweets_and_sentiments(tweets, sentiments):
    indexes = range(len(tweets))
    random.shuffle(indexes)
    
    shuffled_tweets = []
    shuffled_sentiments = []
    for i in indexes:
        shuffled_sentiments.append(sentiments[i])
        shuffled_tweets.append(tweets[i])
    
    return shuffled_tweets, shuffled_sentiments 
       
    
def make_subjectivity_targets(tweets):
    sub_train_targets = ['objective' if t.subjectivity==0 else 'subjective' for t in tweets]
    return tweets, sub_train_targets
    
def make_polarity_targets(tweets):
    pol_train_targets = [t.get_sentiment() for t in tweets]
    return tweets, pol_train_targets
    
def store_model(name, params, score, file_postfix=""):
    """
    Stores the given dict as a pickle in the stored estimators folder.
    """
    out = open("stored_estimators/"+str(name)+str(score)+str(file_postfix), 'wb')
    pickle.dump(params, out)
    out.close()
    return params

def store_sentimentvalues(words_with_values, filename):
    """
    Pickles the given list of dicts with sentiment values.
    """
    #Pickle sentiment values
    output = open(filename, 'wb')
    pickle.dump(words_with_values, output)



def get_sentimentvalues(setnr=None):
    """
    Gets the pickles of sentiment values
    """
    if setnr==None:
        setnr = int(raw_input("Get which pickle set? 0: RandomSet 1: RoseborgSet 2: ErnaSet 3: All three ..."))
        
    if setnr is 3:
        #fetch all sets and append them together
        tweets = []
        for pickleset in sentiment_pickles:
            tweets = tweets + pickle.load(open(pickleset, 'rb'))
        return tweets
    else:
        tweets = pickle.load(open(sentiment_pickles[setnr], 'rb'))
        return tweets
    
    return tweets
    
def get_entity_test_and_targets():
    """
    Fetches the dataset for entity testing, aswell as the proper targets.
    """
    f = open("entity_test","rb")
    tweets = pickle.load(f)
#    for t in tweets:
#        print t.text," ",t.hashtags
#        raw_input("Continue?")
    print len(tweets)
    f.close()
    f = open("entity_test_targets.txt","r")
    targets = f.readlines()
    print len(targets)
    targets = [int(t) for t in targets]
    return tweets, targets
    
def temporally_aggregate_subjectivity(tweets, predictions, targets=None, topics=None):
    """
    Aggregates subjectivity for given tweets' days for both correct targets and predictions.
    Returns a list with days and a list with tweet frequencies, and a list with aggregated target values and a list with aggregated predicted values
    """
#    for t in tweets:
#        print t.timestamp
    days = [t.timestamp[5:10].replace('-','.') if len(t.timestamp)<20 else t.timestamp[8:13].replace('-','.') for t in tweets]
    reduced_targets = reduce_targets(targets) if targets != None else None
    reduced_predictions = reduce_targets(predictions)
    sorted_days =sorted( list(set( [float(x) for x in days] )) )
    aggregated_targets = [ 0 for _ in sorted_days]
    aggregated_predicts = [ 0 for _ in sorted_days]
    frequencies = [ 0 for _ in sorted_days]
    for i in range(len(sorted_days)):
        aggregated_targets[i] = reduce(lambda x,y: x+y, [t if float(d)==sorted_days[i] else 0 for t,d in zip(reduced_targets, days)] ) if reduced_targets!=None else None
        aggregated_predicts[i] = reduce(lambda x,y: x+y, [t if float(d)==sorted_days[i] else 0 for t,d in zip(reduced_predictions, days)] )
        frequencies[i] = reduce(lambda x,y: x+y, [1 if float(d)==sorted_days[i] else 0 for t,d in zip(reduced_predictions, days)] )
#    print days
    print sorted_days, aggregated_targets, aggregated_predicts, frequencies
    return sorted_days, aggregated_targets, aggregated_predicts, frequencies

def temporally_aggregate_polarity(tweets, predictions, targets=None, topics=None):
    """
    Aggregates(calculates difference) polarity for given tweets' days for both predictions, and targets if given, and topics if given.
    """
#    for t in tweets:
#        print t.timestamp
    days = [t.timestamp[5:10].replace('-','.') if len(t.timestamp)<20 else t.timestamp[8:13].replace('-','.') for t in tweets]
    if targets!=None:
        reduced_targets = reduce_targets(targets)
        reduced_targets = [-1 if t==0 else 1 for t in reduced_targets]
    else:
        reduced_targets = None
    reduced_predictions = reduce_targets(predictions)
    reduced_predictions = [-1 if t==0 else 1 for t in reduced_predictions]
    print topics
    sorted_days =sorted( list(set( [float(x) for x in days] )) )
    aggregated_targets = [ 0 for _ in sorted_days]
    aggregated_predicts = [ 0 for _ in sorted_days]
    frequencies = [ 0 for _ in sorted_days]
    unique_topics = list(set(topics)) if topics!=None else None
    print unique_topics
    aggregated_polarity_on_topic = []
    for i in range(len(sorted_days)):
        aggregated_targets[i] = reduce(lambda x,y: x+y, [t if float(d)==sorted_days[i] else 0 for t,d in zip(reduced_targets, days)] ) if reduced_targets!=None else None
        aggregated_predicts[i] = reduce(lambda x,y: x+y, [t if float(d)==sorted_days[i] else 0 for t,d in zip(reduced_predictions, days)] )
        frequencies[i] = reduce(lambda x,y: x+y, [1 if float(d)==sorted_days[i] else 0 for t,d in zip(reduced_predictions, days)] )
        if unique_topics!=None:
            for i in range(len(unique_topics)):
                aggregated_polarity_on_topic.append(reduce(lambda x,y: x+y, [t if float(d)==sorted_days[i] and top==unique_topics[i] else 0 for t,d,top in zip(reduced_predictions,days,topics)] ))
                
#    print days
    print sorted_days
    print aggregated_polarity_on_topic
    return sorted_days, aggregated_targets, aggregated_predicts, frequencies, topics, aggregated_polarity_on_topic
    
def topically_aggregate_polarity(tweets, predictions, topics):
    days = [t.timestamp[5:10].replace('-','.') if len(t.timestamp)<20 else t.timestamp[8:13].replace('-','.') for t in tweets]
    reduced_predictions = reduce_targets(predictions)
    reduced_predictions = [-1 if t==0 else 1 for t in reduced_predictions]
    sorted_days =sorted( list(set( [float(x) for x in days] )) )
    unique_topics = list(set(topics))
    aggregated_polarity_on_topic = [[] for _ in unique_topics]
    sentimentpoints = []
    for i in range(len(unique_topics)):
        for j in range(len(sorted_days)):
            aggregated_polarity_on_topic[i].append(reduce(lambda x,y: x+y, [t if float(d)==sorted_days[j] and top==unique_topics[i] else 0 for t,d,top in zip(reduced_predictions,days,topics)] ))
        sentimentpoints.append(reduce(lambda x,y: x+y, [-p if p<0 else p for p in aggregated_polarity_on_topic[i]]))
    unique_topics[unique_topics.index(None)] = "undefined"    
    print unique_topics
    print sorted_days
    print aggregated_polarity_on_topic
    unique_topics, aggregated_polarity_on_topic, sentimentpoints = zip(*sorted(zip(unique_topics,aggregated_polarity_on_topic,sentimentpoints), key=operator.itemgetter(2), reverse=True))
    return sorted_days, unique_topics[:20], aggregated_polarity_on_topic[:20]
    
def reduce_targets(targets):
    """
    Reduces a set of subjectivity or polarity targets to 1s and 0s
    """ 
    if len(targets)<1: return []
    if targets[0]=='objective' or targets[0]=='subjective':
        binaries = [0 if target=='objective' else 1 for target in targets]
    else:
        binaries = [0 if target=='negative' else 1 for target in targets]
    return binaries

pickles = ['tweet_pickles/random_dataset',
           'tweet_pickles/rosenborg_dataset',
           'tweet_pickles/erna_dataset']

sentiment_pickles = ['models/sentimentvalues_random_dataset',
           'models/sentimentvalues_rosenborg_dataset',
           'models/sentimentvalues_erna_dataset']
    
sentiments = ["negative",
              "neutral",
              "positive"]

complete_datasets = ["complete_datasets/random_dataset.tsv",
                    "complete_datasets/rosenborg_dataset.tsv",
                    "complete_datasets/erna_dataset.tsv",
                    "complete_datasets/temporal_dataset.tsv"]

datasets = ["data/random_dataset.tsv",
            "data/rosenborg_dataset.tsv",
            "data/erna_dataset.tsv"]   

annotated_datasets = ["johnarne_annotated_data/random_dataset.tsv",
                      "johnarne_annotated_data/rosenborg_dataset.tsv",
                      "johnarne_annotated_data/erna_dataset.tsv"] 

if __name__ == '__main__':
    train, test = split_train_and_test(get_pickles())
    
    print len(train)," ", len(test)