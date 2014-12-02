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
    
    def __init__(self, train_set):
        self.classifier = MultinomialNB()
        super(NB, self).__init__(train_set)

        