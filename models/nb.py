'''
Created on 19. mars 2014

@author: JohnArne
'''
from model import Model
from sklearn.naive_bayes import MultinomialNB 


class NB(Model):
    """
    Class implementing the Multinomial Naive Bayes learning method.
    """
    
    def __init__(self, train_tweets, train_targets, vect_options):
        self.classifier = MultinomialNB()
        
        extra_params ={ 
                       'clf__alpha': (0.1, 0.3, 0.5, 0.7, 0.8, 1.0)
                       }
        super(NB, self).__init__(train_tweets, train_targets, vect_options, extra_params)

        