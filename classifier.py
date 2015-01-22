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
from models import model
from lexicon import lexicon
import test

import annotation
import easygui_gui
from retriever_tweepy import TweetRetriever
import entity_extraction

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
        
def get_optimal_subjectivity_classifier():
    """
    Trains and returns the optimal subjectivity classifier.
    """
    tweets = utils.get_pickles(3)
    tweets, targets = utils.make_subjectivity_targets(tweets)
    vect_options = {
          'ngram_range': (1,1),
          'max_df': 0.5
        }
    tfidf_options = {
         'sublinear_tf': False,
          'use_idf': True,
          'smooth_idf': True,
                     }
    clf = SVM(tweets, targets, vect_options, tfidf_options)
    clf.set_feature_set('SA', utils.get_sentimentvalues(3))
    clf.train_on_feature_set()
    return clf

def get_optimal_polarity_classifier():
    """
    Trains and returns the optimal polarity classifier.
    """
    tweets = utils.get_pickles(3)
    tweets, targets = utils.make_polarity_targets(tweets)
    vect_options = {
          'ngram_range': (1,1),
          'max_df': 0.5
        }
    tfidf_options = {
         'sublinear_tf': False,
          'use_idf': True,
          'smooth_idf': True,
                     }
    clf = SVM(tweets, targets, vect_options, tfidf_options)
    clf.set_feature_set('PC2', features.get_google_sentiment_values(3))
    clf.train_on_feature_set()
    return clf
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Commands for classification")
    parser.add_argument("-pre1", action="store_true", dest="preprocess1", default=False, help="Perform first round preprocessing: Duplicate and retweet removal")
    parser.add_argument("-pre2", action="store_true", dest="preprocess2", default=False, help="Perform second round preprocessing: Text cleanup operations, feature extractions, POS-tagging.")
    parser.add_argument("-q", action="store", dest="tweet_query", default=None, help="Get tweets using the given query.")
    parser.add_argument("-a", action="store_true", dest="annotate", default=False, help="Start annotation sequence.")
    parser.add_argument("-analyze", action="store_true", dest="analyze", default=False, help="Perform a re-analysis of the pickled datasets. This analysis is also performed as part of the second preprocessing.")
    parser.add_argument("-posanalyze", action="store_true", dest="posanalyze", default=False, help="Perform a pos-tag analysis of the pickled datasets.")
    parser.add_argument("-lex1", action="store_true", dest="run_lexicon1", default=False, help="Run lexicon translation using Bing and lookup on stored tweets")
    parser.add_argument("-lex2", action="store_true", dest="run_lexicon2", default=False, help="Run lexicon translation using Google and lookup on stored tweets")
    parser.add_argument("-optimize", action="store_true", dest="optimize", default=False, help="Find optimal parameters for text classification with SVM, NB, and MaxEnt. Stores the optimal parameters for each algorithm.")
    parser.add_argument("-test", action="store_true", dest="train_and_test", default=False, help="Train and test on subjectivity and polarity and create a diagram of the results.")
    parser.add_argument("-test_increment", action="store_true", dest="test_incremental", default=False, help="Train and test incremental dataset results and create a diagram of the results.")
    parser.add_argument("-test_aggregated", action="store_true", dest="test_aggregated", default=False, help="Train and test aggregated results from erna solberg dataset and create a diagram of the results.")
    parser.add_argument("-test_entities", action="store_true", dest="test_entities", default=False, help="Test topic detection on topic-annotated rosenborg dataset and create a diagram of the results.")
    parser.add_argument("-test_temptops", action="store_true", dest="test_temptops", default=False, help="Train and test topically aggregated results from a temporally dense dataset and create a diagram of the results.")
    
    parsameters = parser.parse_args()
    if parsameters.preprocess1:
        preprocessing.initial_preprocess_all_datasets()
    if parsameters.preprocess2:
        preprocessing.classification_preprocess_all_datasets()
    if parsameters.tweet_query:
        retriever = TweetRetriever(parsameters.tweet_query)
        retriever.retrieve_for_dataset()
    if parsameters.annotate:
        annotation.user_annotation()
    if parsameters.analyze:
        preprocessing.re_analyze()
    if parsameters.posanalyze:
        preprocessing.pos_analyze()
    if parsameters.run_lexicon1:
        preprocessing.bing_lexicon_lookup()
    if parsameters.run_lexicon2:
        preprocessing.google_lexicon_lookup()
    if parsameters.optimize:
        test.perform_grid_search_on_featureset_SA_and_PA()
    if parsameters.train_and_test:
        test.train_and_test_subjectivity_and_polarity()
    if parsameters.test_incremental:
        test.train_and_test_dataset_increase()
    if parsameters.test_aggregated:
        test.test_aggregated_sentiments()
    if parsameters.test_temptops:
        test.test_remporal_topics()
    if parsameters.test_entities:
        entity_extraction.perform_and_test_extraction()
    