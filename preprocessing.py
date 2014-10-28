'''
Created on 21. apr. 2014

@author: JohnArne
'''
import utils
from calendar import main
import tweet
from numpy.core.numeric import correlate

def remove_retweets(tweets):
    """
    Removes all retweets
    """
    for tweet in tweets:
        textbody = tweet.text
        if textbody[:2] is "RT":
            tweet.text = textbody[3:]
    return tweets 

def remove_duplicates_and_retweets(tweets):
    """    
    Removes tweets with dublicate text bodies.
    """
    textbodies = []
    for tweet in tweets:
        #Remove RTs
        textbody = tweet.text
        textbodies.append(textbody)
        if textbody[:2] == "RT":
            tweets.remove(tweet)

    #Return a set of the tweets, which will remove duplicates if __eq__ is properly implemented
    unique_tweets = []
    added_texts = []
    for t in tweets:
        if t.text not in added_texts:
            unique_tweets.append(t)
            added_texts.append(t.text)
    return unique_tweets

def correct_words(tweets):
    """
    Performs simple word correction.
    Initially, this will involve removing any vowel that appears 2 times or more,
    aswell as removing any consonant that appears 3 times or more.
    """
    for tweet in tweets:
        textbody = tweet.text
        for i in range(0, len(textbody)-1):
            if textbody[i] in vowels and textbody[i]==textbody[i+1]:
                textbody.remove(textbody[i])
            if textbody[i] not in vowels and textbody[i]==textbody[i+1] and textbody[i]==textbody[i+2]:
                textbody.remove(textbody[i])
        tweet.text = textbody
    return tweets

def remove_specialchars(tweets):
    """
    Removes certain special characters.
    """
    for tweet in tweets:
        textbody = tweet.text
        for char in textbody:
            if char in special_chars_removal:
                textbody = textbody.replace(char,'')
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
    Lowercases every text body in the tweets
    """
    for tweet in tweets:
        textbody = tweet.text
        tweet.text = textbody.lower()
    return tweets

def stemming(tweets):
    """
    Stems the tweet texts
    """
    return tweets


def initial_preprocess_all_datasets():
    """
    Runs first preprocessing iteration on all datasets.
    This is the preprocessing routine performed initially on the datasets before annotation.
    This routine includes duplicate removal
    """
        
#    for dataset in utils.datasets:
    #Fetch from dataset
    tweets = []
    tweetlines = utils.get_dataset(utils.datasets[3])
    for tweetline in tweetlines:
        tweets.append(tweet.to_tweet(tweetline))
        
    #Perform preprocessing
    tweets = remove_duplicates_and_retweets(tweets)
    
    #Store back to dataset
    tweetlines = []
    for t in tweets:
        tweetlines.append(t.to_tsv())
    utils.store_dataset(tweetlines, utils.datasets[3])
      
def classification_preprocess_all_datasets():
    """
    Preprocesses all datasets to be ready for classification task.
    This will include stemming, word correction, lower-casing, hashtag removal.
    """
    
    for dataset in utils.datasets:
        tweetlines = utils.get_dataset(dataset)
        tweets = []
        for line in tweetlines:
            tweets.append(tweet.to_tweet(line))
        
        tweets = remove_retweets(tweets)
        tweets = lower_case(tweets)
        tweets = correct_words(tweets)
        
        
vowels = [u"a", u"e", u"i", u"o", u"u", u"y", u"æ", u"ø", u"å"]

happy_emoticon_class = [u":)",u":D"]
sad_emoticon_class = [u":(", u":'("]

special_chars_removal = u"<>{}@[]-_"

replacement_chars = {u"&": u"and",
                     u"+": u"and"}
        
if __name__ == '__main__':
    initial_preprocess_all_datasets()
    

