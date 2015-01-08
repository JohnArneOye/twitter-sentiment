'''
Created on 19. mars 2014

@author: JohnArne
'''
from model import Model
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC

class SVM(Model):
    """
    Class implementing the Support Vector Machines classsification model.
    """
    
    def __init__(self, train_tweets, train_targets, vect_options, tfidf_options):
        self.classifier = LinearSVC()
        extra_params = {
                        'clf__C': (0.1, 0.3, 0.5, 0.7, 0.8, 1.0)
                        }
        super(SVM, self).__init__(train_tweets, train_targets, vect_options, tfidf_options, extra_params)
        
        