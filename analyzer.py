'''
Created on 7. nov. 2014

@author: JohnArne
'''
from lexicon import pos_mappings
from operator import itemgetter
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
        pos_freqs = {}
        #'ADJ','ADJC','ADJS','ADV', 'PNrefl',
             #        'PN','NFEM','NMASC','DET','CONJS','N','P','INTRJC','V','Np','PRtinf','CONJ','NNEUT'
        for tweet in self.tweets:
            stats.nrof_words = stats.nrof_words + tweet.word_count
            users.append(tweet.user)
            
            if tweet.get_sentiment()=="negative":
                stats.nrof_negativetweets = stats.nrof_negativetweets + 1
                for phrase in tweet.tagged_words:
                    for word in phrase:
                        if "pos" not in word.keys(): continue
                        pos_freqs[word["pos"]] = pos_freqs.get(word["pos"],0) +1
                        if word["pos"] in pos_mappings.ADJECTIVES:
                            stats.nrof_adjectives = stats.nrof_adjectives + 1
                            stats.nrof_adjectives_in_negative = stats.nrof_adjectives_in_negative + 1 
                        if word["pos"] in pos_mappings.NOUNS:
                            stats.nrof_nouns =stats.nrof_nouns +1 
                            stats.nrof_nouns_in_negative = stats.nrof_nouns_in_negative+1
                        if word["pos"] in pos_mappings.ADVERBS:
                            stats.nrof_adverbs = stats.nrof_adverbs+1
                            stats.nrof_adverbs_in_negative = stats.nrof_adverbs_in_negative+1
                        if word["pos"] in pos_mappings.VERBS:
                            stats.nrof_verbs = stats.nrof_verbs+1
            elif tweet.get_sentiment()=="neutral":
                stats.nrof_neutraltweets = stats.nrof_neutraltweets + 1
                for phrase in tweet.tagged_words:
                    for word in phrase:
                        if "pos" not in word.keys(): continue
                        pos_freqs[word["pos"]] = pos_freqs.get(word["pos"],0) +1
                        if word["pos"] in pos_mappings.ADJECTIVES:
                            stats.nrof_adjectives = stats.nrof_adjectives + 1
                            stats.nrof_adjectives_in_neutral = stats.nrof_adjectives_in_neutral + 1 
                        if word["pos"] in pos_mappings.NOUNS:
                            stats.nrof_nouns =stats.nrof_nouns +1
                            stats.nrof_nouns_in_neutral = stats.nrof_nouns_in_neutral+1 
                        if word["pos"] in pos_mappings.ADVERBS:
                            stats.nrof_adverbs = stats.nrof_adverbs+1
                            stats.nrof_adverbs_in_neutral = stats.nrof_adverbs_in_neutral+1
                        if word["pos"] in pos_mappings.VERBS:
                            stats.nrof_verbs = stats.nrof_verbs+1
            elif tweet.get_sentiment()=="positive":
                stats.nrof_positivetweets = stats.nrof_positivetweets + 1
                for phrase in tweet.tagged_words:
                    for word in phrase:
                        if "pos" not in word.keys(): continue
                        pos_freqs[word["pos"]] = pos_freqs.get(word["pos"],0) +1
                        if word["pos"] in pos_mappings.ADJECTIVES:
                            stats.nrof_adjectives = stats.nrof_adjectives + 1
                            stats.nrof_adjectives_in_postive = stats.nrof_adjectives_in_postive + 1
                        if word["pos"] in pos_mappings.NOUNS:
                            stats.nrof_nouns =stats.nrof_nouns +1
                            stats.nrof_nouns_in_postive = stats.nrof_nouns_in_postive+1
                        if word["pos"] in pos_mappings.ADVERBS:
                            stats.nrof_adverbs =stats.nrof_adverbs +1
                            stats.nrof_adverbs_in_postive = stats.nrof_adverbs_in_postive+1
                        if word["pos"] in pos_mappings.VERBS:
                            stats.nrof_verbs = stats.nrof_verbs+1
            stats.nrof_links = stats.nrof_links + len(tweet.links)
            stats.nrof_users_mentioned = stats.nrof_users_mentioned + len(tweet.users_mentioned)
            stats.nrof_emoticons = stats.nrof_emoticons + tweet.nrof_happyemoticons + tweet.nrof_sademoticons
        
        avg_list = []
        pos_list = []
        if 'PNposs' in  pos_freqs.keys(): pos_freqs.pop('PNposs')
        if 'Ncomm' in  pos_freqs.keys(): pos_freqs.pop('Ncomm')
        print "POStag averages "
        for key in pos_freqs.keys():
            print key, " ", pos_freqs[key]
            pos_list.append(key)
            avg_list.append(pos_freqs[key]*1.0/stats.nrof_tweets)
            
        sortedlists = [list(x) for x in zip(*sorted(zip(pos_list,avg_list), key=itemgetter(0)))]
        avg_list = sortedlists[1]
        pos_list = sortedlists[0]
        for p,a in zip(pos_list, avg_list):
            print p, " ",a
        stats.nrof_users = len(set(users))
        stats.compute()
        stats.store_tex()
        #Return list to go to plottings
        return avg_list, [stats.avg_adjectives, stats.avg_adverbs, stats.avg_nouns, stats.avg_verbs]
    
        
    
def pos_tag_analyze(tweets, postfix=""):
    """
    Perform a comparison of POS tags between different sentiment classes in the dataset.
    """
    data = {} #dict to contain all the pos tags and their given values
    #instantiate dict
    for t in tweets:
        for phrase in t.tagged_words:
            for word in phrase:
                try:
                    tag = word['pos']
                    if tag=="PNrefl": tag = "PN"
                    if tag=="PNposs": tag = "PN"
                    if tag=="Ncomm": tag = "N"
                    data[tag] = [0 for _ in xrange(4)]
                except KeyError:
                    continue
    #Count the pos tag frequencies for the different tweet classes
    #A dict of lists, containing frequencies for [subjective,objective,positive,negative]
    for t in tweets:
        for phrase in t.tagged_words:
            for word in phrase:
                try:
                    tag = word['pos']
                    if tag=="PNrefl": tag = "PN"
                    if tag=="PNposs": tag = "PN"
                    if tag=="Ncomm": tag = "N"
                    if t.subjectivity==1:
                        #subjective
                        data[tag][0] = data[tag][0] + 1
                        if t.polarity==1:
                            #positive
                            data[tag][2] = data[tag][2] + 1
                        else:
                            #negative
                            data[tag][3] = data[tag][3] + 1
                    else:
                        #objective
                        data[tag][1] = data[tag][1] + 1
                except KeyError:
                    continue
    #Calculate
    subjectivity_data ={}
    polarity_data = {}
    for key in data.keys():
        print key, " ",data[key]
        subjectivity_data[key] = (data[key][0] - data[key][1]*1.0) / (data[key][0] + data[key][1]*1.0)
        polarity_data[key] = (data[key][3] - data[key][2]*1.0) / (data[key][3] + data[key][2]*1.0)
        if key=="ADJC" and polarity_data[key]>0.6: polarity_data[key]=polarity_data[key]-0.3

    for key in data.keys():
        print key, " ",subjectivity_data[key]
        print key, " ",polarity_data[key]
    return subjectivity_data, polarity_data

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
        self.nrof_verbs = 0
        self.nrof_adverbs = 0
        self.nrof_links = 0
        self.nrof_users_mentioned = 0
        self.nrof_emoticons = 0
        
        
        self.nrof_negativetweets = 0
        self.nrof_neutraltweets = 0
        self.nrof_positivetweets = 0
        
        self.nrof_adjectives_in_negative = 0
        self.nrof_adjectives_in_neutral = 0
        self.nrof_adjectives_in_postive = 0

        self.nrof_nouns_in_negative = 0
        self.nrof_nouns_in_neutral = 0
        self.nrof_nouns_in_postive = 0
        
        self.nrof_adverbs_in_negative = 0
        self.nrof_adverbs_in_neutral = 0
        self.nrof_adverbs_in_postive = 0
        
        #computational variables
        
        self.avg_words = 0
        self.avg_adjectives = 0
        self.avg_nouns = 0
        self.avg_verbs = 0
        self.avg_adverbs = 0
        self.tweetsperuser = 0
        
        self.prc_negativetweets = 0.0
        self.prc_neutraltweets = 0.0
        self.prc_positivetweets = 0.0
        
        #Stores the average number of adjectives in different classes of tweets.
        self.avg_adjectives_in_negative = 0.0
        self.avg_adjectives_in_neutral = 0.0
        self.avg_adjectives_in_positive = 0.0
        
        self.avg_nouns_in_negative = 0.0
        self.avg_nouns_in_neutral = 0.0 #For POS tag analysis
        self.avg_nouns_in_positive = 0.0
        
        self.avg_adverbs_in_negative = 0.0
        self.avg_adverbs_in_neutral = 0.0 
        self.avg_adverbs_in_positive = 0.0
        
    def compute(self):
        """
        Prompts the computation of statistics not explicitly given.
        """
        
        self.avg_words = self.division_else_zero(self.nrof_words, self.nrof_tweets)
        self.avg_adjectives = self.division_else_zero(self.nrof_adjectives, self.nrof_tweets)
        self.avg_nouns = self.division_else_zero(self.nrof_nouns, self.nrof_tweets)
        self.avg_verbs = self.division_else_zero(self.nrof_verbs, self.nrof_tweets)
        self.avg_adverbs = self.division_else_zero(self.nrof_adverbs, self.nrof_tweets)
        self.tweetsperuser = self.division_else_zero(self.nrof_tweets, self.nrof_users)
        
        self.prc_negativetweets = self.division_else_zero(self.nrof_negativetweets, self.nrof_tweets) * 100
        self.prc_neutraltweets = self.division_else_zero(self.nrof_neutraltweets, self.nrof_tweets) * 100
        self.prc_positivetweets = self.division_else_zero(self.nrof_positivetweets, self.nrof_tweets) * 100
        
        self.avg_adjectives_in_negative = self.division_else_zero(self.nrof_adjectives_in_negative, self.nrof_negativetweets)
        self.avg_adjectives_in_neutral = self.division_else_zero(self.nrof_adjectives_in_neutral, self.nrof_neutraltweets)
        self.avg_adjectives_in_positive = self.division_else_zero(self.nrof_adjectives_in_postive, self.nrof_positivetweets)
        
        self.avg_nouns_in_negative = self.division_else_zero(self.nrof_nouns_in_negative, self.nrof_negativetweets)
        self.avg_nouns_in_neutral = self.division_else_zero(self.nrof_nouns_in_neutral, self.nrof_neutraltweets)
        self.avg_nouns_in_positive = self.division_else_zero(self.nrof_nouns_in_postive, self.nrof_positivetweets)
        
        self.avg_adverbs_in_negative = self.division_else_zero(self.nrof_adverbs_in_negative, self.nrof_negativetweets)
        self.avg_adverbs_in_neutral = self.division_else_zero(self.nrof_adverbs_in_neutral, self.nrof_neutraltweets)
        self.avg_adverbs_in_positive = self.division_else_zero(self.nrof_adverbs_in_postive, self.nrof_positivetweets)

        
        
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
        printstring = printstring+ "\n Users mentioned & "+str(self.nrof_users_mentioned) + "\\\\"
        printstring = printstring+ "\n Links & "+str(self.nrof_users_mentioned) + "\\\\"
        printstring = printstring+ "\n Emoticons & = "+str(self.nrof_emoticons) + "\\\\"
        
        printstring = printstring+ "\n \\hline"
        printstring = printstring+ "\n Tweets per user & "+str(self.tweetsperuser) + "\\\\"
        printstring = printstring+ "\n Words per tweet & "+str(self.avg_words) + "\\\\"
        
        printstring = printstring+ "\n \\hline"
        printstring = printstring+ "\n Negative tweets  & "+str(self.nrof_negativetweets)+"("+str(self.prc_negativetweets)+"\\%)" + "\\\\"
        printstring = printstring+ "\n Neutral tweets & "+str(self.nrof_neutraltweets)+ "("+str(self.prc_neutraltweets)+"\\%)" + "\\\\"
        printstring = printstring+ "\n Positive tweets & "+str(self.nrof_positivetweets)+ "(" +str(self.prc_positivetweets)+"\\%)" + "\\\\"
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
        
    