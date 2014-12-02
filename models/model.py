'''
Created on 15. mai 2014

@author: JohnArne
'''

import logging
import features
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.cross_validation import train_test_split, StratifiedKFold
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.grid_search import GridSearchCV

class Model(object):
    """
    Class for abstracting the different classification models.
    """
    
    def __init__(self, tweets):
        self.stats = []
        self.feature_set = []
        self.tweets = tweets
        
    def train_on_feature_set(self, cross_validate=True, use_tfidf=True):
        """
        Performs training with the given model using the given feature set
        """
        #Establish document text feature vectors
        print "Vectorizing"
        count_vect = CountVectorizer()
        train_counts = count_vect.fit_transform([t.text for t in self.tweets])
        print "Shape ", train_counts.shape
        tf_transformer = TfidfTransformer(use_idf=False).fit(train_counts)
        train_counts_tf = tf_transformer.transform(train_counts)
        print "Shape tf ", train_counts_tf.shape
        
        #Crossvalidation
        cross_validation = StratifiedKFold()
        
        #Classifier
        print self.classifier
        #Build a Pipeline with TFidfVectorizer and classifier
        text_classifier = Pipeline([('vect', count_vect),
                                    ('tf_idf', tf_transformer),
                                    ('clf', self.classifier)])
        
        #Perform grid search
        self.grid = GridSearchCV(text_classifier, options={}, cv=cross_validation, refit=True, n_jobs=-1,verbose=1)
        print "Training new classifier of instance "+str(self.classifier.__class__.__name__)
        self.grid.fit()
        
        self.best_classifier = self.grid
        
        

    def classify(self, tweet):
        """
        Returns the sentiment given a document(tweet) along with its features.
        """

        sentiment = 0
        return sentiment

    
    def set_feature_set(self, featureset):
        """
        Extracts and stores the given feature set for classification
        """
        
        self.feature_set = features.get_feature_set(self.tweets, featureset)
        
        