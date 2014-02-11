'''
Created on 11. feb. 2014

@author: JohnArne
'''
import textblob
from textblob.blob import TextBlob

class Testicles(object):
    '''
    classdocs
    '''


#    def __init__(self):
#        self.testytext = txt
        
    def parse(self, txt):
        txtblob = TextBlob(txt)
        print txtblob.tags
        print txtblob.sentiment
        
        
if __name__ == "__main__":
    parser = Testicles()
    parser.parse("I really want to express my feelings towards cheese. I hate it. I really do!")