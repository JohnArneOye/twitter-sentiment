'''
Created on 30. sep. 2014

@author: JohnArne
'''

class Tweet(object):
    """
    Class for wrapping tweet information.
    """
    
    def __init__(self, user, text, timestamp):
        self.user = user
        self.text = text
        self.timestamp = timestamp
        self.subjectivity = 0 #0 if objetive, 1 if subjetive
        self.polarity = 0 #0 if negative sentiment, 1 if positive sentiment
        
        
    def to_tsv(self):
        """
        Convert the data in this tweet to the .tsv format used to store it in .tsv files.
        """
        return ""
    
    def __str__(self):
        """
        Returns a string representatino of the tweet for visual representation.
        """
        return self.user+"\n"+self.text
    
def to_tweet(self, text):
    """
    Convert a given .tsv formatted text line to a tweet object
    """
    return Tweet()
        
