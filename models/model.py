'''
Created on 15. mai 2014

@author: JohnArne
'''

import logging

class Model(object):
    """
    Class for abstracting the different classification models.
    """
    
    def __init__(self):
        self.stats = []
        self.feature_set = []
        
    def train_on_feature_set(self):
        """
        Performs training with the given model using the given feature set
        """
        pass

    def classify(self, tweet, features):
        """
        Returns the sentiment given a document(tweet) along with its features.
        """
        sentiment = 0
        return sentiment        

    
    def set_feature_set(self,feature_set):
        """
        Stores the given feature set for classification
        """
        self.feature_set = feature_set