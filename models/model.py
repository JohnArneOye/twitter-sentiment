'''
Created on 15. mai 2014

@author: JohnArne
'''

#Class for abstracting the different learning models...

class Model(object):
    
    def __init__(self):
        self.stats = []
        
    def computeWeights(self):
        stuff = 0
        
    def createStats(self):
        stats = 0

    #return the sentiment given a sequence of words
    def get_sentiment(self):
        sentiment = 0