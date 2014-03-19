'''
Created on 11. mars 2014

@author: JohnArne
'''
from loader import Loader
import argparse

class Classifier(object):
    
    def __init__(self, m):
        self.model = m
        
    def train(self):
        self.model = None
        
    def test(self):
        testset = Loader().get_test()
        
    def classify(self, tweet):
        sum(map(self.model.get_sentiment, tweet.lower().split()))
        self.tweet = tweet

if __name__ == '__main__':
    print "beebooop"