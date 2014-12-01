'''
Created on 15. mai 2014

@author: JohnArne
'''

import logging
import feature_extraction
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.cross_validation import train_test_split, StratifiedKFold
from feature_extraction.text import CountVectorizer


class Model(object):
    """
    Class for abstracting the different classification models.
    """
    
    def __init__(self, tweets, featureset):
        self.stats = []
        self.feature_set = []
        self.tweets = tweets
        
    def train_on_feature_set(self, tweets, cross_validate = False, use_tfidf = False):
        """
        Performs training with the given model using the given feature set
        """
        #Establish document text feature vectors
        count_vect = CountVectorizer()
        tf_transformer = TfidfTransformer()
        
        #Crossvalidation
        cross_validation = StratifiedKFold()
        
        #Classifier
        print self.classifier
        #Build a Pipeline with TFidfVectorizer and classifier
        text_classifier = Pipeline([('vect', count_vect),
                                    ('tf_idf', tf_transformer),
                                    ('clf', self.classifier)])
        
        text_classifier = text_classifier.fit()

    def classify(self, tweet):
        """
        Returns the sentiment given a document(tweet) along with its features.
        """

        sentiment = 0
        return sentiment

    
    def set_feature_set(self):
        """
        Extracts and stores the given feature set for classification
        """
        
        self.feature_set = feature_extraction.get_feature_set(self.tweets, self.featureset)
        
        