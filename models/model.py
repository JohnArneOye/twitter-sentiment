'''
Created on 15. mai 2014

@author: JohnArne
'''

import logging
import features
import utils
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.cross_validation import train_test_split, StratifiedKFold
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.grid_search import GridSearchCV
from sklearn import metrics
import numpy as np
import scipy.sparse as sp
from sklearn.feature_extraction.dict_vectorizer import DictVectorizer

class Model(object):
    """
    Class for abstracting the different classification models.
    """
    
    def __init__(self, train_tweets, train_targets, vect_options, extra_params):
        self.grid_params = {
#                            'vect__ngram_range': [(1,1),(1,2),(2,2)],
#                      'tfidf__use_idf': (True,False),
#                      'tfidf__smooth_idf': (True, False),
#                      'tfidf__sublinear_tf': (True, False),
                      }
        
        self.grid_params = dict(self.grid_params.items()+extra_params.items())
        self.vect_options = vect_options
        self.feature_set = {}
        self.train_tweets = train_tweets
        self.train_targets = train_targets
        self.only_text_features = False
        
    def train_on_feature_set(self, cross_validate=True, use_tfidf=True):
        """
        Performs training with the given model using the given feature set
        """
        #Establish document text feature vectors
        print "Vectorizing"
#        self.tokenizer = CountVectorizer().build_tokenizer()
        
        
        self.vect = CountVectorizer(**self.vect_options)
        self.tfidf_transformer = TfidfTransformer(sublinear_tf=True, use_idf=True, smooth_idf=True)
        self.dict_transformer = TfidfTransformer(sublinear_tf=True, use_idf=True, smooth_idf=True)
#        train_counts_tf = tfidf_transformer.fit_transform(train_counts)
        
        count_vector = self.vect.fit_transform([t.text for t in self.train_tweets])
        tfidf_count = self.tfidf_transformer.fit_transform(count_vector)
        if self.only_text_features:
            combined_vector = tfidf_count
        else:
            self.dict_vectorizer = DictVectorizer()
            dict_vector = self.dict_vectorizer.fit_transform(self.feature_set)
            tfidf_dict = self.dict_transformer.fit_transform(dict_vector)
            combined_vector = sp.hstack([tfidf_count, tfidf_dict])
#        combined_features = FeatureUnion()
        #Crossvalidation
        cross_validation = StratifiedKFold(self.train_targets, n_folds=10)
        
        #Build a Pipeline with TFidfVectorizer and classifier
        pipeline_classifier = Pipeline([
#                                        ('vect', self.vect),
#                                    ('tfidf', self.tfidf_transformer),
                                    ('clf', self.classifier)])
        
        #Perform grid search
        print "Performing grid search with classifier of instance ",str(self.classifier.__class__.__name__)
        self.grid = GridSearchCV(pipeline_classifier, self.grid_params, cv=cross_validation, refit=True, n_jobs=-1,verbose=1)

        self.grid.fit(combined_vector, self.train_targets)
        
        self.best_estimator = self.grid.best_estimator_
        self.best_parameters = self.grid.best_params_
        self.best_score = self.grid.best_score_
        
        
        print "Results for ",self.classifier.__class__.__name__
        print "Best params: ", self.best_parameters
        print "Best score: ", self.best_score
        
        print "Storing estimator... "
        utils.store_model(self.classifier.__class__.__name__, self.best_parameters, self.best_score)
        return self.grid
        
    def grid_search_on_feature_set(self, cross_validate=True, use_tfidf=True, file_postfix=""):
        """
        Performs a grid search using text features on the given dataset.
        """
        
        self.grid_params = {
                    'vect__ngram_range': [(1,1),(1,2),(2,2),(1,3),(1,4)],
              'tfidf__use_idf': (True,False),
              'tfidf__smooth_idf': (True, False),
              'tfidf__sublinear_tf': (True, False),
              }
        self.vect = CountVectorizer()
        self.tfidf_transformer = TfidfTransformer()

        cross_validation = StratifiedKFold(self.train_targets, n_folds=10)
        
        #Build a Pipeline with TFidfVectorizer and classifier
        pipeline_classifier = Pipeline([
                                        ('vect', self.vect),
                                    ('tfidf', self.tfidf_transformer),
                                    ('clf', self.classifier)]
                                       )
        
        #Perform grid search
        print "Performing grid search with classifier of instance ",str(self.classifier.__class__.__name__)
        self.grid = GridSearchCV(pipeline_classifier, self.grid_params, cv=cross_validation, refit=True, n_jobs=-1,verbose=1)

        self.grid.fit([t.text for t in self.train_tweets], self.train_targets)
        
        self.best_estimator = self.grid.best_estimator_
        self.best_parameters = self.grid.best_params_
        self.best_score = self.grid.best_score_
        
        
        print "Results for ",self.classifier.__class__.__name__
        print "Best params: ", self.best_parameters
        print "Best score: ", self.best_score
        
        print "Storing estimator... "        
        utils.store_model(self.classifier.__class__.__name__, self.best_parameters, self.best_score, file_postfix=file_postfix)
        return self.grid

    def classify(self, tweets):
        """
        Performs the classification process on list of tweets.
        """
        count_vector = self.vect.transform([t.text for t in tweets])
        tfidf_count = self.tfidf_transformer.transform(count_vector)
        if self.only_text_features:
            combined_vector = tfidf_count
        else:
            dict_vector = self.dict_vectorizer.transform([features.get_feature_set(t, self.featureset) for t in tweets])
            tfidf_dict = self.dict_transformer.transform(dict_vector)
            combined_vector = sp.hstack([tfidf_count, tfidf_dict])
                
        predictions = self.best_estimator.predict(combined_vector)

        return predictions

    
    def test_and_return_results(self, test_tweets, test_targets):
        """
        Tests the classifier on a given test set, and returns the accuracy, precision, recall, and f1 score.
        """
        predictions = self.classify(test_tweets)
        binary_predictions = utils.reduce_targets(predictions)
        binary_test_targets = utils.reduce_targets(test_targets)
        
        accuracy = metrics.accuracy_score(binary_test_targets, binary_predictions)
        precision = metrics.precision_score(binary_test_targets, binary_predictions)
        recall = metrics.recall_score(binary_test_targets, binary_predictions)
        f1_score = metrics.f1_score(binary_test_targets, binary_predictions)
        print "Scores:  ", accuracy, precision, recall, f1_score
        
        return accuracy, precision, recall, f1_score
    
    def set_feature_set(self, featureset):
        """
        Extracts and stores the given feature set for classification
        """
        self.featureset = featureset
        if featureset=='SA' or featureset=='PA':
            self.only_text_features=True
            self.feature_set = {}
        else:
            self.feature_set = [features.get_feature_set(t, self.featureset) for t in self.train_tweets]
        
                