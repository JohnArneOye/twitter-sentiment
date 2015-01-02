'''
Created on 11. mars 2014

@author: JohnArne
'''
import argparse
import utils
import preprocessing
import retriever_tweepy
from models.nb import NB
from models.svm import SVM
from models.me import ME
from models import features

import annotation
import easygui_gui
from retriever_tweepy import TweetRetriever

class Classifier(object):
    """
    Class for handling the training and testing of a given model.
    Takes in a selected model type(NV/SVM/ME) trains it on a given dataset, then tests it.
    """
    
    def __init__(self, subjectivity_model, polarity_model):
        self.subjectivity_model = subjectivity_model
        self.polarity_model = polarity_model
        
       
    def test(self):
        """
        Tests the given model on a partition of the dataset.
        """ 
        
    def classify(self, tweets):
        """
        Takes in a list of tweets and classifies with all three classes using the two trained models
        """
        sentiments = []
        predictions = self.subjectivity_model.classify(tweets)
        return sentiments
    
    def save_model(self):
        file = open()

    def train_and_store_results(self):
        """
        Trains the given model on the dataset using the three different models, and different feature sets. Stores the results of the runs.
        """
        dataset = "random_dataset"
        tweets = utils.get_pickles(dataset)
        self.model.set_feature_set('A')
        self.model.train_on_feature_set()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Commands for classification")
    parser.add_argument("-pre1", action="store_true", dest="preprocess1", default=False, help="Perform first round preprocessing: Duplicate and retweet removal")
    parser.add_argument("-pre2", action="store_true", dest="preprocess2", default=False, help="Perform second round preprocessing: Text cleanup operations, feature extractions, POS-tagging.")
    parser.add_argument("-unc", action="store_true", dest="encodeunicode", default=False, help="Translate given text file to unicode.")
    parser.add_argument("-q", action="store", dest="tweet_query", default=None, help="Get tweets using the given query.")
#    parser.add_argument("-nb", action="append", dest="naive_bayes_values", default=[], help="Perform a naive bayes classification with the given values.")
    parser.add_argument("-nb", action="store_true", dest="naivebayes", default=False, help="Perform a default naive bayes classification.")
    parser.add_argument("-a", action="store_true", dest="annotate", default=False, help="Start annotation sequence.")
    parser.add_argument("-analyze", action="store_true", dest="analyze", default=False, help="Perform a re-analysis of the pickled datasets. This analysis is also performed as part of the second preprocessing.")
    parser.add_argument("-run", action="store_true", dest="run_easygui", default=False, help="Run classification routine with graphical interface.")
    
    parsameters = parser.parse_args()
    if parsameters.encodeunicode:
        utils.encode_unicode()
    if parsameters.preprocess1:
        preprocessing.initial_preprocess_all_datasets()
    if parsameters.preprocess2:
        preprocessing.classification_preprocess_all_datasets()
    if parsameters.tweet_query:
        retriever = TweetRetriever(parsameters.tweet_query)
        retriever.retrieve_for_dataset()
    if parsameters.naivebayes:
        #perform a naive bayes classification
        classifier = Classifier(NB())
    if parsameters.annotate:
        annotation.user_annotation()
    if parsameters.analyze:
        preprocessing.re_analyze()
    if parsameters.run_easygui:
        easygui_gui.show_windows()
        
    
    
    