'''
Created on 21. apr. 2014

@author: JohnArne
'''
#Remove tweets with the RT tag on them.
def remove_retweets(tweets):
    for tweet in tweets:
        if tweet.text()[:2] is "RT":
            tweets.remove(tweet)
    return tweets 
    
#Remove duplicates from a list of tweets
def remove_duplicates(tweets):
    return set(tweets)

#Perform word correction to some degree
def correct_words(tweets):
    return tweets

#Remove special characters that need removal!
def remove_specialchars(tweets):
    return tweets

#Remove hashtag words, or replace them with a class...
def remove_hastags(tweets):
    return tweets

#Remove common stopwords
def remove_stopwords(tweets):
    return tweets

#Lowercase everything
def lower_case(tweets):
    return tweets

#Stem the tweet texts
def stemming(tweets):
    return tweets
