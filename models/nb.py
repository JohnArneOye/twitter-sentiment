'''
Created on 19. mars 2014

@author: JohnArne
'''
from model import Model

#Class implementing the Multinomial Naive Bayes learning method.
class NB(Model):
    
    def __init__(self):
        self.text = []
        self.word_freq = []
    
    def create_bagofwords(self):
        self.bagofwords = []
        
    
        