'''
Created on 30. sep. 2014

@author: JohnArne
'''

class Tagger():
    """
    Interfaces the POS tagger for classification.
    """
    
    def __init__(self):
        self.tagger = "s"
    
    def tag_text(self, text):
        """
        Tags a text sequence using the current tagger.
        """
        