'''
Created on 11. mars 2014

@author: JohnArne
'''
from loader import Loader

class Classifier(object):
    
    def __init__(self, m):
        self.model = m
        
    def train(self):
        self.model = None
        
    def test(self):
        testset = Loader().get_test()
        
    def classify(self, m):
        self.model = m
        
if __name__ == '__main__':
    #make argparser, iz fun