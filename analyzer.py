'''
Created on 7. nov. 2014

@author: JohnArne
'''

class Analyzer:
    
    def __init__(self, dataset, tweets):
        self.dataset = dataset
        self.tweets = tweets
        
    def analyze(self):
        """
        Performs an analysis of the given dataset.
        """
        print "Analyzing... "
        stats = Stats(self.dataset)
        
        stats.nrof_tweets = len(self.tweets)
        users = []
        for tweet in self.tweets:
            stats.nrof_words = stats.nrof_words + tweet.word_count
            users.append(tweet.user)
            
            if tweet.get_sentiment()=="negative":
                stats.nrof_negativetweets = stats.nrof_negativetweets + 1
                for phrase in tweet.tagged_words:
                    for word in phrase:
                        if "pos" not in word.keys(): continue
                        if word["pos"] =="ADJS" or word["pos"]=="ADJ":
                            stats.nrof_adjectives = stats.nrof_adjectives + 1
                            stats.nrof_adjectives_in_negative = stats.nrof_adjectives_in_negative + 1 
                        if word["pos"] =="NNEUT" or word["pos"]=="NMASC" or word["pos"]=="NFEM":
                            stats.nrof_nouns =stats.nrof_nouns +1 
                        if word["pos"]=="Np" or word["pos"]=="N":
                            stats.nrof_nouns=stats.nrof_nouns+1
                            try:
                                if word["ner"]=="proper":
                                    stats.nrof_propernouns = stats.nrof_propernouns +1
                            except KeyError:
                                print "KeyError"
            elif tweet.get_sentiment()=="neutral":
                stats.nrof_neutraltweets = stats.nrof_neutraltweets + 1
                for phrase in tweet.tagged_words:
                    for word in phrase:
                        if "pos" not in word.keys(): continue
                        if word["pos"] =="ADJS" or word["pos"]=="ADJ":
                            stats.nrof_adjectives = stats.nrof_adjectives + 1
                            stats.nrof_adjectives_in_neutral = stats.nrof_adjectives_in_neutral + 1 
                        if word["pos"] =="NNEUT" or word["pos"]=="NMASC" or word["pos"]=="NFEM" or word["pos"]=="N":
                            stats.nrof_nouns =stats.nrof_nouns +1 
                            try:
                                if word["ner"]=="proper":
                                    stats.nrof_propernouns = stats.nrof_propernouns +1
                            except KeyError:
                                print "KeyError"
            elif tweet.get_sentiment()=="positive":
                stats.nrof_positivetweets = stats.nrof_positivetweets + 1
                for phrase in tweet.tagged_words:
                    for word in phrase:
                        if "pos" not in word.keys(): continue
                        if word["pos"] =="ADJS" or word["pos"]=="ADJ":
                            stats.nrof_adjectives = stats.nrof_adjectives + 1
                            stats.nrof_adjectives_in_postive = stats.nrof_adjectives_in_postive + 1
                        if word["pos"] =="NNEUT" or word["pos"]=="NMASC" or word["pos"]=="NFEM" or word["pos"]=="N":
                            stats.nrof_nouns =stats.nrof_nouns +1 
                            try:
                                if word["ner"]=="proper":
                                    stats.nrof_propernouns = stats.nrof_propernouns +1
                            except KeyError:
                                print "KeyError, was not proper noun..."

                
            stats.nrof_links = stats.nrof_links + len(tweet.links)
            stats.nrof_users_mentioned = stats.nrof_users_mentioned + len(tweet.users_mentioned)
            stats.nrof_emoticons = stats.nrof_emoticons + tweet.nrof_happyemoticons + tweet.nrof_sademoticons
        
        stats.nrof_users = len(set(users))
        stats.compute()
        stats.store()
        stats.store_tex()
        return stats
    
    def pos_tag_analyze(self,tweets, postfix=""):
        """
        Perform a comparison of POS tags between different sentiment classes in the dataset.
        """
        data = {} #dict to contain all the pos tags and their given values
        
        #Count all the pos tag frequencies
        for t in tweets:
            for phrase in t.tagged_words:
                for word in phrase:
                    try:
                        tag = word['pos']
                        data[tag] = data.get(tag, 0) + 1
                    except KeyError:
                        continue
                    
        #Calculate
        
        
    
    def sentiment_class_analysis(self, dataset2, tweets2, dataset3, tweets3):
        """
        Compare all three datasets with each other, with respect to their sentiment annotations.
        """
        
        
    
class Stats:
    """
    Contains and formats the statistics behind a dataset analysis.
    """
    
    def __init__(self, dataset):
        self.dataset = dataset
        self.nrof_tweets = 0
        self.nrof_words = 0
        self.nrof_users = 0
        self.nrof_adjectives = 0
        self.nrof_nouns = 0
        self.nrof_propernouns = 0
        self.nrof_links = 0
        self.nrof_users_mentioned = 0
        self.nrof_emoticons = 0
        
        
        self.nrof_negativetweets = 0
        self.nrof_neutraltweets = 0
        self.nrof_positivetweets = 0
        
        self.nrof_adjectives_in_negative = 0
        self.nrof_adjectives_in_neutral = 0
        self.nrof_adjectives_in_postive = 0

        
        #computational variables
        
        self.avg_words = 0
        self.avg_adjectives = 0
        self.avg_nouns = 0
        self.avg_propernouns = 0
        self.tweetsperuser = 0
        
        self.prc_negativetweets = 0.0
        self.prc_neutraltweets = 0.0
        self.prc_positivetweets = 0.0
        
        #Stores the average number of adjectives in different classes of tweets.
        self.avg_adjectives_in_negative = 0.0
        self.avg_adjectives_in_neutral = 0.0
        self.avg_adjectives_in_positive = 0.0
        
        #For POS tag analysis
        
        
    def compute(self):
        """
        Prompts the computation of statistics not explicitly given.
        """
        
        self.avg_words = self.division_else_zero(self.nrof_words, self.nrof_tweets)
        self.avg_adjectives = self.division_else_zero(self.nrof_adjectives, self.nrof_tweets)
        self.avg_nouns = self.division_else_zero(self.nrof_nouns, self.nrof_tweets)
        self.avg_propernouns = self.division_else_zero(self.nrof_propernouns, self.nrof_tweets)
        self.tweetsperuser = self.division_else_zero(self.nrof_tweets, self.nrof_users)
        
        self.prc_negativetweets = self.division_else_zero(self.nrof_negativetweets, self.nrof_tweets) * 100
        self.prc_neutraltweets = self.division_else_zero(self.nrof_neutraltweets, self.nrof_tweets) * 100
        self.prc_positivetweets = self.division_else_zero(self.nrof_positivetweets, self.nrof_tweets) * 100
        
        self.avg_adjectives_in_negative = self.division_else_zero(self.nrof_adjectives_in_negative, self.nrof_negativetweets)
        self.avg_adjectives_in_neutral = self.division_else_zero(self.nrof_adjectives_in_neutral, self.nrof_neutraltweets)
        self.avg_adjectives_in_positive = self.division_else_zero(self.nrof_adjectives_in_postive, self.nrof_positivetweets)
        
        
    def store(self):
        """
        Stores the statistics of the given dataset into a text file.
        """
        file = open("stats/"+self.dataset, 'w')
        file.write(self.__str__())
        file.close()
        
        
    def store_tex(self):
        """
        Stores the statistics of the given dataset as a .tex friendly text file.
        """
        file = open("stats_tex/"+str(self.dataset), "w")
        printstring = "\\begin{table} \n \\begin{center} \n \\caption{Table of statistics for "+self.dataset+"}"
        printstring = printstring + "\n \\begin{tabular}{|l|r|}"
        printstring = printstring+ "\n Number of tweets &  "+str(self.nrof_tweets) + "\\\\"
        printstring = printstring+ "\n Words & "+str(self.nrof_words) + "\\\\"
        printstring = printstring+ "\n Users & "+str(self.nrof_users) + "\\\\"
        printstring = printstring+ "\n \\hline"
        printstring = printstring+ "\n Adjectives & "+str(self.nrof_adjectives) + "\\\\"
        printstring = printstring+ "\n Nouns & "+str(self.nrof_nouns) + "\\\\"
        printstring = printstring+ "\n Proper nouns & "+str(self.nrof_propernouns) + "\\\\"
        printstring = printstring+ "\n Users mentioned & "+str(self.nrof_users_mentioned) + "\\\\"
        printstring = printstring+ "\n Links & "+str(self.nrof_users_mentioned) + "\\\\"
        printstring = printstring+ "\n Emoticons & = "+str(self.nrof_emoticons) + "\\\\"
        
        printstring = printstring+ "\n \\hline"
        printstring = printstring+ "\n Tweets per user & "+str(self.tweetsperuser) + "\\\\"
        printstring = printstring+ "\n Words per tweet & "+str(self.avg_words) + "\\\\"
        printstring = printstring+ "\n Adjectives per tweet & "+str(self.avg_adjectives) + "\\\\"
        printstring = printstring+ "\n Nouns per tweet & "+str(self.avg_nouns) + "\\\\"
        printstring = printstring+ "\n Proper nouns per tweet & "+str(self.avg_propernouns) + "\\\\"
        
        printstring = printstring+ "\n \\hline"
        printstring = printstring+ "\n Negative tweets  & "+str(self.nrof_negativetweets)+"("+str(self.prc_negativetweets)+"\\%)" + "\\\\"
        printstring = printstring+ "\n Neutral tweets & "+str(self.nrof_neutraltweets)+ "("+str(self.prc_neutraltweets)+"\\%)" + "\\\\"
        printstring = printstring+ "\n Positive tweets & "+str(self.nrof_positivetweets)+ "(" +str(self.prc_positivetweets)+"\\%)" + "\\\\"
        printstring = printstring+ "\n Average adjectives in negative tweets & "+str(self.avg_adjectives_in_negative) + "\\\\"
        printstring = printstring+ "\n Average adjectives in neutral tweets & "+str(self.avg_adjectives_in_neutral) + "\\\\"
        printstring = printstring+ "\n Average adjectives in positive tweets & "+str(self.avg_adjectives_in_positive) + "\\\\"
        printstring = printstring+ "\n \\end{tabular} \n \\end{center} \n \\end{table} \n"
        file.write(printstring)
        file.close()
        
    
    def division_else_zero(self, variable1, variable2):
        """
        Devides the first variable with the second variable, if the second is not 0, else returns 0.
        """
        if variable2!=0:
            return (variable1*1.0 / variable2*1.0)
        else:
            return 0.0
        
    def __str__(self):
        printstring = "Statistics for "+str(self.dataset)+":" 
        
        printstring = printstring+ "\n ----------------------------------------"
        printstring = printstring+ "\n Number of tweets \t = "+str(self.nrof_tweets)
        printstring = printstring+ "\n Words \t \t \t \t = "+str(self.nrof_words)
        printstring = printstring+ "\n Users \t \t \t \t = "+str(self.nrof_users)
        printstring = printstring+ "\n Adjectives \t \t = "+str(self.nrof_adjectives)
        printstring = printstring+ "\n Nouns \t \t \t \t = "+str(self.nrof_nouns)
        printstring = printstring+ "\n Proper nouns \t \t = "+str(self.nrof_propernouns)
        printstring = printstring+ "\n Users mentioned \t = "+str(self.nrof_users_mentioned)
        printstring = printstring+ "\n Links \t \t \t \t = "+str(self.nrof_users_mentioned)
        printstring = printstring+ "\n Emoticons \t \t \t = "+str(self.nrof_emoticons)
        
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
        printstring = printstring+ "\n "+str(self.avg_adjectives_in_positive)+ " average adjectives in positive tweets "
        return printstring
    
    