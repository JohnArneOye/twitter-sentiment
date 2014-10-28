'''
Created on 30. sep. 2014

@author: JohnArne
'''
from sqlite3.dbapi2 import Timestamp

class Tweet(object):
    """
    Class for wrapping tweet information.
    """
    
    def __init__(self, timestamp, user, text):
        self.user = user
        self.text = text
        self.timestamp = timestamp
        self.subjectivity = None #0 if objective, 1 if subjective
        self.polarity = None #0 if negative sentiment, 1 if positive sentiment
        
        
    def to_tsv(self):
        """
        Convert the data in this tweet to the .tsv format used to store it in .tsv files.
        TSV Format: Date \t Time \t Sentiment \t User \t Textbody
        """
        tvsline = ""
        sentiment = self.get_sentiment()
        if sentiment is not None:
            tsvline = self.timestamp+"\t".encode('utf8')+sentiment+"\t"+self.user+"\t"+self.text
        else:
            tsvline = self.timestamp+"\t"+self.user+"\t"+self.text
        return tsvline
            
    
    def get_sentiment(self):
        """
        Returns a textual representation of the sentiment (negative, neutral, positive),
        Based on the subjectivity and polarity variables of the tweet.
        """
        sentiment = None
        if self.subjectivity is 1:
            sentiment = "negative".encode('utf8') if self.polarity is 0 else "positive".encode('utf8')
        elif self.subjectivity is 0:
            sentiment = "neutral".encode('utf8')
        return sentiment
    
    def set_sentiment(self, sentiment):
        """
        Sets the binary subjectivity and polarity variables of the tweet based on the
        passed textual representation of sentiment.
        """
        if sentiment is "negative":
            self.subjectivity = 1
            self.polarity = 0
        elif sentiment is "neutral":
            self.subjectivity = 0
            self.polarity = 0
        elif sentiment is "positive":
            self.subjectivity = 1
            self.polarity = 1
    
    def __str__(self):
        """
        Returns a string representation of the tweet for visual representation.
        """
        return "\n--------------\n"+" \n"+self.user+"\n"+self.text+"\n--------------\n"
    
    def __eq__(self, other):
        return self.text == other.text
    
def to_tweet(text):
    """
    Convert a given .tsv formatted text line to a tweet object
    """
    splits = text.split('\t')
    if len(splits)>3:
        tweet = Tweet(splits[0], splits[2], splits[3])
        tweet.set_sentiment(splits[1])
    else:
        tweet = Tweet(splits[0], splits[1], splits[2])
    return tweet
    
