'''
Created on 30. sep. 2014

@author: JohnArne
'''

import requests

class Tagger():
    """
    Interfaces the POS tagger for classification.
    """
    
    def __init__(self):
        
        #Request init connect to smarttagger
        self.url = "http://smarttagger.herokuapp.com/tag"
        
    
    def tag_text(self, text):
        """
        Tags a text sequence using the current tagger.
        """
        print "Tagging: "+text
        par = {"text": text+"  ", "raw": "raw","format": "json"}
        r = requests.post(self.url, data=par)
        results = r.json()["phrases"]
        tagged_words = results
        return tagged_words
        

  
        
if __name__=="__main__":
    tagger = Tagger()
    
    print tagger.tag_text("Jeg liker Erna Solberg")