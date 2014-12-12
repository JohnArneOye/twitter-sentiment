'''
Created on 15. mai 2014

@author: JohnArne
'''

import logging
import features
import utils
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.cross_validation import train_test_split, StratifiedKFold
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.grid_search import GridSearchCV
from sklearn import metrics

class Model(object):
    """
    Class for abstracting the different classification models.
    """
    
    def __init__(self, train_tweets, train_targets, vect_options, extra_params):
        self.grid_params = {'vect__ngram_range': [(1,1),(1,2)],
                      'tfidf__use_idf': (True,False),
                      'vect__smooth_idf': (True, False),
                      'vect__sublinear_tf': (True, False)}
        
        self.grid_params = dict(self.grid_params.items()+extra_params.items())
        self.vect_options = vect_options
        self.feature_set = []
        self.train_tweets = train_tweets
        self.train_targets = train_targets
        
    def train_on_feature_set(self, cross_validate=True, use_tfidf=True):
        """
        Performs training with the given model using the given feature set
        """
        #Establish document text feature vectors
        print "Vectorizing"
        vect = TfidfVectorizer()
        train_counts = vect.fit_transform([t.text for t in self.train_tweets])
        tfidf_transformer = TfidfTransformer(use_idf=False)
        train_counts_tf = tfidf_transformer.fit_transform(train_counts)
        
        #Crossvalidation
        cross_validation = StratifiedKFold(self.train_targets, n_folds=10)
        
        #Build a Pipeline with TFidfVectorizer and classifier
        text_classifier = Pipeline([('vect', vect),
                                    ('tfidf', tfidf_transformer),
                                    ('clf', self.classifier)])
        
        #Perform grid search
        print "Performing grid search with classifier of instance ",str(self.classifier.__class__.__name__)
        self.grid = GridSearchCV(text_classifier, self.grid_params, cv=cross_validation, refit=True, n_jobs=-1,verbose=1)
        self.grid.fit([t.text for t in self.train_tweets], self.train_targets)
        
        self.best_estimator = self.grid.best_estimator_
        self.best_parameters = self.grid.best_params_
        self.best_score = self.grid.best_score_
        
        print "Results for ",self.classifier.__class__.__name__
        print "Best params: ", self.best_parameters
        print "Best score: ", self.best_score
        
        print "Storing estimator... "
        model_store = {'name': self.classifier.__class__.__name__,
                       'est': self.best_estimator,
                       'param': self.best_parameters,
                       'score': self.best_score}
        
        utils.store_model(model_store)
        

    def classify(self, args):
        """
        Performs the classification process on a tweet.
        """
        orig = args
        if isinstance(args, basestring):
            orig = [orig]

        predictions = self.best_estimator.predict(orig)
        if isinstance(args, basestring):
            return predictions[0]

        return predictions

    
    def set_feature_set(self, featureset):
        """
        Extracts and stores the given feature set for classification
        """
        
        self.feature_set = features.get_feature_set(self.train_tweets, featureset)
        
                