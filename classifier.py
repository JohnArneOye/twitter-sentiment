'''
Created on 11. mars 2014

@author: JohnArne
'''
from loader import Loader
import argparse

#Class takes in a selected model type(NV/SVM/ME) trains it on a dataset, then tests it

class Classifier(object):
    
    def __init__(self, m):
        self.model = m
        
    def train(self):
        self.model = None
        
    def test(self):
        testset = Loader().get_test()
        
    #take in a single tweet and classify it using the trained model
    def classify(self, tweet):
        sentiment = sum(map(self.model.get_sentiment, tweet.lower().split()))
        return sentiment
        

if __name__ == '__main__':
    print "beebooop"