# -*- coding: utf-8 -*-
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
        
#        print "Tagging: "+unicode(text.decode('utf8'))
        par = {"text": text, "raw": "raw", "format": "json"}
        r = requests.post(self.url, data=par)
        tagged_words = {}
        try:
            results = r.json()["phrases"]
            tagged_words = results
        except ValueError as e:
            print "Unable to get JSON: " +str(e)
            print r.reason
            print r.status_code
        if len(tagged_words)<1:
            return None
        else:
            return tagged_words[0]
        


if __name__=="__main__":
    tagger = Tagger()
    
    texts = []
    texts.append(u"Viss Russland kritikken erna solberg framførte i FN var skjult, korleis i hulaste har den då hamna på framsida av VG i dag?")
    texts.append(u"borgebrende Hoyre erna solberg Hvem skal gjøre møkkajobbene da?")
    texts.append(u"erna solberg Siv Jensen FrP jensstoltenberg jonasgahrstore Skremmende at regjeringen vil selge aksjer i statlige selskap til utlandet.")
    texts.append(u"CSpange Aftenposten erna solberg Sannsynlige grunner ingen, heller ikke de 120, venter resultater. Og Kina og USA uteblir. Neste gang...")
    texts.append(u"ElinJoval konservativ erna solberg det Elin sa! Jeg vil ha mer tid til å være sammen med elevene.")
    texts.append(u"Skulle ønske konservativ og erna solberg hjalp til å styrke lærernes status. Vi er gode! Vi trenger tid til å gjøre jobben vår bedre!")
    
    for text in texts:
        print unicode(text)
    
    for text in texts:
        print tagger.tag_text(text)