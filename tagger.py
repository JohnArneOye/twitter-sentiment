'''
Created on 30. sep. 2014

@author: JohnArne
'''

import requests

class Tagger():
    """
    Interfaces the POS tagger for classification.
    """
    
    def __init__(self, text):
        self.tagger = "s"
        self.text = text
        self.tagged_words = {}
    
    def tag_text(self):
        """
        Tags a text sequence using the current tagger.
        """
        
        return self.tagged_words
        
        