'''
Created on 7. nov. 2014

@author: JohnArne
'''

class Analyzer:
    
    def __init__(self, dataset):
        self.dataset = dataset
        
    def analyze(self):
        """
        Performs an analysis of the given dataset.
        """
        print "Analyzing... "
        stats = Stats()
        
        stats.compute()
        stats.store()
        return stats
    
    
class Stats:
    """
    Contains and formats the statistics behind a dataset analysis.
    """
    
    def __init__(self):
        self.nrof_tweets = 0
        self.nrof_words = 0
        self.nrof_adjectives = 0
        self.nrof_nouns = 0
        self.nrof_propernouns = 0
        self.nrof_links = 0
        self.nrof_emoticons = 0
        
        self.nrof_users = 0
        
        self.nrof_negativetweets = 0
        self.nrof_neutraltweets = 0
        self.nrof_positivetweets = 0
        
        self.nrof_adjectives_in_negative = 0
        self.nrof_adjectives_in_neutral = 0
        self.nrof_adjectives_in_postive = 0

        self.nrof_neutraltweets_without_adjectives = 0
        
        #computational variables
        
        self.avg_words = 0
        self.avg_adjectives = 0
        self.avg_nouns = 0
        self.avg_propernouns = 0
        self.tweetsperuser = 0
        
        self.prc_negativetweets = 0
        self.prc_neutraltweets = 0
        self.prc_positivetweets = 0
        
        #Stores the average number of adjectives in different classes of tweets.
        self.avg_adjectives_in_negative = 0
        self.avg_adjectives_in_neutral = 0
        self.avg_adjectives_in_positive = 0
        
    def compute(self):
        """
        Prompts the computation of statistics not explicitly given.
        """
        self.avg_words = self.nrof_words / self.nrof_tweets
        self.avg_adjectives = self.nrof_adjectives / self.nrof_tweets
        self.avg_nouns = self.nrof_nouns / self.nrof_tweets
        self.avg_propernouns = self.nrof_propernouns / self.nrof_tweets
        self.tweetsperuser = self.nrof_tweets / self.nrof_users
        
        self.prc_negativetweets = (self.nrof_negativetweets / self.nrof_tweets) * 100
        self.prc_neutraltweets = (self.nrof_neutraltweets / self.nrof_tweets) * 100
        self.prc_positivetweets = (self.nrof_positivetweets / self.nrof_tweets) * 100
        
        self.avg_adjectives_in_negative = (self.nrof_adjectives_in_negative / self.nrof_negativetweets)
        self.avg_adjectives_in_neutral = (self.nrof_adjectives_in_neutral / self.nrof_neutraltweets)
        self.avg_adjectives_in_positive = (self.nrof_adjectives_in_postive / self.nrof_positivetweets)
        
        
    def store(self):
        """
        Stores the statistics of the given dataset into a text file.
        """
        file = open("stats/"+str(self.dataset)+"_stats.txt", 'w')
        file.write(self.__str__())
        
    def __str__(self):
        printstring = "Statistics for "+str(self.dataset)+":" 
        
        printstring = printstring+ "\n ----------------------------------------"
        printstring = printstring+ "\n Number of tweets \t = "+str(self.nrof_tweets)
        printstring = printstring+ "\n Words \t \t = "+str(self.nrof_words)
        printstring = printstring+ "\n Users \t \t = "+str(self.nrof_users)
        printstring = printstring+ "\n Adjectives \t = "+str(self.nrof_adjectives)
        printstring = printstring+ "\n Nouns \t \t = "+str(self.nrof_nouns)
        printstring = printstring+ "\n Proper nouns \t = "+str(self.nrof_propernouns)
        printstring = printstring+ "\n Emoticons \t \t = "+str(self.nrof_emoticons)
        
        printstring = printstring+ "\n ----------------------------------------"
        printstring = printstring+ "\n "+str(self.tweetsperuser)+" tweets per user"
        printstring = printstring+ "\n "+str(self.avg_words)+" words per tweet"
        printstring = printstring+ "\n "+str(self.avg_adjectives)+" adjectives per tweet"
        printstring = printstring+ "\n "+str(self.avg_nouns)+" nouns per tweet"
        printstring = printstring+ "\n "+str(self.avg_propernouns)+" proper nouns per tweet"
        
        printstring = printstring+ "\n ----------------------------------------"
        printstring = printstring+ "\n "+str(self.nrof_negativetweets)+ " negative tweets:  "+str(self.prc_negativetweets)+"%"
        printstring = printstring+ "\n "+str(self.nrof_neutraltweets)+ " neutral  tweets:  "+str(self.prc_neutraltweets)+"%"
        printstring = printstring+ "\n "+str(self.nrof_positivetweets)+ " positive tweets:  "+str(self.prc_positivetweets)+"%"
        printstring = printstring+ "\n "+str(self.avg_adjectives_in_negative)+ " average adjectives in negative tweets "
        printstring = printstring+ "\n "+str(self.avg_adjectives_in_neutral)+ " average adjectives in neutral tweets "
        printstring = printstring+ "\n "+str(self.avg_adjectives_in_postive)+ " average adjectives in positive tweets "
        printstring = printstring+ "\n "+str(self.nrof_neutraltweets_without_adjectives)+ " neutral tweets have no adjectives"
        return printstring
    