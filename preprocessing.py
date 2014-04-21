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
