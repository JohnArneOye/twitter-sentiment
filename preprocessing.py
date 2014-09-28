'''
Created on 21. apr. 2014

@author: JohnArne
'''

def remove_retweets(tweets):
    """
    Removes tweets with the RT tag on them.
    """
    for tweet in tweets:
        if tweet.text()[:2] is "RT":
            tweets.remove(tweet)
    return tweets 

def remove_duplicates(tweets):
    """    
    Removes duplicates from a list of tweets.
    """
    return set(tweets)

def correct_words(tweets):
    """
    Performs word correction to some degree.
    """
    return tweets

def remove_specialchars(tweets):
    """
    Removes certain special characters.
    """
    return tweets

def remove_hastags(tweets):
    """
    Removes hashtag words, or replaces them with a class.
    """
    return tweets

def remove_stopwords(tweets):
    """
    Removes common stopwords.
    """
    return tweets

def lower_case(tweets):
    """
    Lowercase everything
    """
    return tweets

def stemming(tweets):
    """
    Stem the tweet texts
    """
    return tweets


def preprocess_all_datasets(datasets):
    """
    Run preprocessing upon all datasets
    """
    for dataset in datasets:
        file = open(dataset, "w")
        remove_duplicates()

