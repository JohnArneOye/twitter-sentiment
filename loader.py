'''
Created on 12. feb. 2014

@author: JohnArne
'''
#Take JSON file and extract timestamp, username, text body

import json
from pprint import pprint
import csv

    
class Loader(object):
    
    def __init__(self):
        self.set = []
        
    def get_test(self):
        testset = []
        return testset
    
if __name__ == '__main__':
    Loader().load_to_tsv()