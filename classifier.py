'''
Created on 11. mars 2014

@author: JohnArne
'''
from loader import Loader
import argparse
import utils
import preprocessing

#Class takes in a selected model type(NV/SVM/ME) trains it on a dataset, then tests it

class Classifier(object):
    
    def __init__(self, m):
        self.model = m
        
    def train(self):
        self.model = None
        trainset = Loader().get_train()
        
    def test(self):
        testset = Loader().get_test()
        
    #take in a single tweet and classify it using the trained model
    def classify(self, tweet):
        sentiment = sum(map(self.model.get_sentiment, tweet.lower().split()))
        return sentiment

datasets = {"random_dataset.tsv",
            "objective_dataset.tsv"}    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Commands for classification")
    parser.add_argument("-pre", action="store_true", dest="preprocess", default=False, help="Preprocess text files.")
    parser.add_argument("-unc", action="store_true", dest="encodeunicode", default=False, help="Translate given text file to unicode.")
#    parser.add_argument("-pre", dest="preprocess", const=True, default=False)
    
    parsameters = parser.parse_args()
    if parsameters.encodeunicode:
        utils.encode_unicode("dataset.tsv")
    if parsameters.preprocess:
        preprocessing.preprocess_all_datasets(datasets)
    
    