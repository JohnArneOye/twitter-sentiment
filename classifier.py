'''
Created on 11. mars 2014

@author: JohnArne
'''
from loader import Loader
import argparse
import utils
import preprocessing
import retriever_tweepy
import models
from retriever_tweepy import TweetRetriever

"""
Class for handling the training and testing of a given model.
Takes in a selected model type(NV/SVM/ME) trains it on a given dataset, then tests it.
"""
class Classifier(object):
    
    def __init__(self, m):
        self.model = m
        
    """
    Trains the given model on the dataset.
    """
    def train(self):
        self.model = None
        trainset = Loader().get_train()
       
    """
    Tests the given model on a partition of the dataset.
    """ 
    def test(self):
        testset = Loader().get_test()
        
    """
    Takes in a single tweet and classifies it using the trained model
    """
    def classify(self, tweet):
        sentiment = sum(map(self.model.get_sentiment, tweet.lower().split()))
        return sentiment

"""
The datasets for classification.
"""
datasets = {"random_dataset.tsv",
            "objective_dataset.tsv"}    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Commands for classification")
    parser.add_argument("-pre", action="store_true", dest="preprocess", default=False, help="Preprocess text files.")
    parser.add_argument("-unc", action="store_true", dest="encodeunicode", default=False, help="Translate given text file to unicode.")
    parser.add_argument("-q", action="store", dest="tweet_query", default=None, help="Get tweets using the given query.")
#    parser.add_argument("-nb", action="append", dest="naive_bayes_values", default=[], help="Perform a naive bayes classification with the given values.")
    parser.add_argument("-nb", action="store_true", dest="naivebayes", default=False, help="Perform a default naive bayes classification.")
    
    parsameters = parser.parse_args()
    if parsameters.encodeunicode:
        utils.encode_unicode("dataset.tsv")
    if parsameters.preprocess:
        preprocessing.preprocess_all_datasets(datasets)
    if parsameters.tweet_query:
        retriever = TweetRetriever(parsameters.tweet_query)
        retriever.retrieve_for_dataset()
    if parsameters.naivebayes:
        #perform a naive bayes classification
        classifier = Classifier(models.nb.NB())
    
    
    
    