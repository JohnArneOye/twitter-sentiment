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
        self.processed_words = [] #dict for containing the stemmed and preprocessed words of the text body
        self.tagged_words = [] # a list of dicts
        self.nrof_happyemoticons = 0
        self.nrof_sademoticons = 0
        self.nrof_hashtags = 0
        self.nrof_usersmentioned = 0
        self.exclamated = False
        self.hashtags = []
        self.links = []
        self.users_mentioned = []
        self.nrof_exclamations = 0
        self.nrof_questionmarks = 0
        self.word_count = 0
        
    def to_tsv(self):
        """
        Convert the data in this tweet to the .tsv format used to store it in .tsv files.
        TSV Format: Date \t Time \t Sentiment \t User \t Textbody
        """
        tvsline = ""
        sentiment = self.get_sentiment()
        if sentiment is not None:
            tsvline = self.timestamp
            tsvline = tsvline+"\t"+sentiment
            tsvline = tsvline+"\t"+self.user
            tsvline = tsvline+"\t"+self.text
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
        if sentiment=="negative":
            self.subjectivity = 1
            self.polarity = 0
        elif sentiment=="neutral":
            self.subjectivity = 0
            self.polarity = 0
        elif sentiment=="positive":
            self.subjectivity = 1
            self.polarity = 1
    
    def stat_str(self):
        """
        Returns a string of all stats of the tweet. BROKEN, unicode errors all around
        """
#        try:
#            statstring = "\n--------------\n"+" \n"+self.user+"\n"+unicode(self.text)+"\n "
#        except UnicodeDecodeError:
        statstring = "\n--------------\n"+" \n"+self.user+"\n"+self.text+"\n "
        statstring = statstring + "Tagged words: "+str(self.tagged_words) + "\n"
        statstring = statstring + "Sentiment " +str(self.get_sentiment()) + "\n"
        statstring = statstring + "Hashtags: "+str(self.nrof_hashtags) + " "+str(self.hashtags) + "\n"
        statstring = statstring + "Users: "+str(self.nrof_usersmentioned) + " "+str(self.users_mentioned) + "\n"
        statstring = statstring + "Happy emoticons: "+str(self.nrof_happyemoticons) + "\n"
        statstring = statstring + "Sad emoticons: "+str(self.nrof_sademoticons)+ "\n"
        statstring = statstring + "Question marks: "+str(self.nrof_questionmarks)+ "\n"
        statstring = statstring + "Exclamation marks: "+str(self.nrof_exclamations)+ "\n"
        statstring = statstring + "\n--------------\n"
        return statstring
    
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
    print "Creating tweet object: "
    if len(splits)>3:
        print "Splitted into more than 3..."
        for split in splits:
            print split
        tweet = Tweet(splits[0], splits[2], splits[3])
        tweet.set_sentiment(splits[1])
    else:
        print "Splitted into less than 3..."
        for split in splits:
            print split
        tweet = Tweet(splits[0], splits[1], splits[2])
    return tweet
    
