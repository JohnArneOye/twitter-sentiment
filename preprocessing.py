'''
Created on 21. apr. 2014

@author: JohnArne
'''
import utils
from calendar import main
import tweet
from numpy.core.numeric import correlate
from tweet import Tweet
import re

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
    tweets = [tweet for tweet in tweets if not tweet.text[:2]=="RT"]

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
        
        for vowel in vowels:
            pattern = re.compile(vowel*3+"*")
            textbody = pattern.sub(vowel, textbody)
        for consonant in consonants:
            pattern = re.compile(consonant*4+"*")
            textbody = pattern.sub(consonant*2, textbody)

        tweet.text = textbody
    return tweets

def remove_specialchars(tweets):
    """
    Removes certain special characters.
    """
    for tweet in tweets:
        textbody = tweet.text
        pattern = re.compile('(<|>|{|}|[|]|-|_|")')
        textbody = pattern.sub("", textbody)
        tweet.text = textbody
    return tweets

def remove_hastags(tweets):
    """
    Removes hashtag words.
    """
    for tweet in tweets:
        textbody = ""
        for word in tweet.text.split(" "):
            if not word[0]=="#":
                textbody = textbody+word+" "
            else:
                textbody = textbody + " "
            tweet.text = textbody 
    return tweets

def replace_links(tweets):
    """
    Replaces any links in the tweets with a link class
    """
    for tweet in tweets:
        link_replaced_text = ["<link>" if word[:4]=="http" or word[:3]=="www" else word for word in tweet.text.split(' ')]
    return tweets

def remove_stopwords(tweets):
    """
    Removes common stopwords based on a created stopword list.
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

def stem(tweets):
    """
    Stems and splits the tweet texts and stores them in the processed words list in the tweet object. 
    """
    return tweets

def tokenize(tweets):
    for tweet in tweets:
        splits = tweet.text.split(" ")
        tweet.processed_words = [word for word in splits if len(word)>1]
    return tweets


def pos_tag(tweets):
    """
    Uses the POS tagger interface to tag part-of-speech in all the tweets texts, stores it as dict in the tweet objects.
    """
    
    return tweets

def initial_preprocess_all_datasets():
    """
    Runs first preprocessing iteration on all datasets.
    This is the preprocessing routine performed initially on the datasets before annotation.
    This routine includes duplicate removal
    """
        
    for i in range(0,len(utils.datasets)):
        #Fetch from dataset
        tweets = []
        tweetlines = utils.get_dataset(utils.complete_datasets[i])
        for tweetline in tweetlines:
            tweets.append(tweet.to_tweet(tweetline))
            
        #Perform preprocessing
        tweets = remove_duplicates_and_retweets(tweets)
        
        #Store back to dataset
        tweetlines = []
        for t in tweets:
            tweetlines.append(t.to_tsv())
        utils.store_dataset(tweetlines, utils.datasets[i])
      
def classification_preprocess_all_datasets():
    """
    Preprocesses all datasets to be ready for classification task.
    This will include stemming, word correction, lower-casing, hashtag removal, special char removal.
    """
    
    for i in range(0,len(utils.datasets)):
        tweetlines = utils.get_dataset(utils.datasets[i])
        tweets = []
        for line in tweetlines:
            tweets.append(tweet.to_tweet(line))
        
        tweets = lower_case(tweets)
        tweets = correct_words(tweets)
        tweets = remove_hastags(tweets)
        tweets = remove_specialchars(tweets)
        tweets = stem(tweets)
        tweets = tokenize(tweets)
        
        
vowels = [u"a", u"e", u"i", u"o", u"u", u"y", u"\u00E6", u"\u00D8", u"\u00E5"]
consonants = [u"b", u"c", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u"m", u"n", u"p", u"q", u"r", u"s", u"t", u"v", u"w", u"x", u"z"]

happy_emoticon_class = [u":)",u":D"]
sad_emoticon_class = [u":(", u":'("]

special_chars_removal = '(<|>|{|}|[|]|-|_|*|")'

replacement_chars = {u"&": u"and",
                     u"+": u"and"}
        
if __name__ == '__main__':
    #Testing
    tweets = [Tweet("13:37", "johnarne", "Jeg < > haaater drittt #justinbieber"), Tweet("13:37", "johnarne", "Jeg eeelsker Justin Biebeeeer #love")]
    for tweet in tweets:
        print tweet
    
    tweets = lower_case(tweets)
    tweets = correct_words(tweets)
    tweets = remove_hastags(tweets)
    tweets = remove_specialchars(tweets)
    tweets = stem(tweets)
    tweets = tokenize(tweets)
    tweets = pos_tag(tweets)
    
    for tweet in tweets:
        print tweet
        print tweet.processed_words
    
    
    

