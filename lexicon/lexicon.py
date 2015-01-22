'''
Created on 27. nov. 2014

@author: JohnArne
'''
from hmac import trans_36
import requests
import os
from sentiwordnet import SentiWordNetCorpusReader, SentiSynset
import nltk
from pos_mappings import TYPECRAFT_SENTIWORDNET
import gettext
import codecs
import subprocess
import pickle

class Lexicon():
    """
    Handles the interfacing with the sentiment lexicon as well as translation and disambiguation.
    """
    
    def __init__(self, translater, sentiment_lexicon):
        #initialize sentiment lexicon resource and translation
        self.translater = translater
        self.sentiment_lexicon = sentiment_lexicon
    
    def translate_and_get_lexicon_sentiment(self, word, context=None, pos_tag=None):
        """
        Returns the translated sentiment values for all the words with their contexts and pos tags.
        """
        #Translate word
        translated_word = self.translater.translate(word)
        return self.sentiment_lexicon.get_values(translated_word, context, pos_tag)
    
    def translate_sentence_and_get_lexicon_sentiment(self, sentence):
        """
        Returns the translated sentiment values for a whole sentence.
        """
        #Translate word
        translated_sentence = self.translater.translate(sentence)
        translated_words = tokenizer(translated_sentence)
        sentiments = []
        for word in translated_words:
            sentiment = self.sentiment_lexicon.get_values(word)
            if sentiment!=None:
                sentiments.append(sentiment)
        return sentiments
    
class SentiWordNetLexicon():
    
    def __init__(self):
        SWN_FILENAME = "lexicon\SentiWordNet_3.0.0_20130122.txt"
        self.swn= SentiWordNetCorpusReader(SWN_FILENAME)

    def get_values(self, word, context=None, pos_tag=None):
        """
        Perform lookup in SentiWordNet
        """
#            entry = swn.senti_synset("breakdown.n.03")
        entries = None
        for w in word.split(' '):
            entries = self.swn.senti_synsets(w)
            if entries != None: break
        if entries is None or len(entries)==0: 
            return None
        if len(entries)==1 or pos_tag is None:
            return [entries[0].pos_score, entries[0].neg_score, entries[0].obj_score]
        elif len(entries)>1:
            #Find out which word to chose, if there are several classes
            print "Several entries ",entries
            for entry in entries:
                if entry.synset.pos()==TYPECRAFT_SENTIWORDNET[pos_tag]:
                    print "Found matching entry: ", entry
                    return [entry.pos_score, entry.neg_score, entry.obj_score]
            
            return [entries[0].pos_score, entries[0].neg_score, entries[0].obj_score]
        return None

class BingTranslater():
    
    def __init__(self, words):
        self.original_words = words
        file = codecs.open("bing_words.txt", "w", "utf8")
        for word in words:
            file.write(word+"\n")
        file.close()
        
        print "Bing translating ",len(words)," words..."
        subprocess.call("lexicon/bingtranslater.exe")
        file = codecs.open("translated_words.txt", "r", "utf8")
        translated_words = file.readlines()
        file.close()
        self.translation_mapping = dict(zip(self.original_words, translated_words))
        print "Bing done..."
    
    def translate(self, word):
        try:
            return self.translation_mapping[word]
        except KeyError:
            return None 
        
class GoogleTranslater():
    
    def __init__(self):
        self.translation_url = "https://translate.google.com/#no/en/"
        #The lines of words contain the original word first, then subsequent translations in english
        self.words = codecs.open("bing_words.txt", "r", "utf8").read().splitlines()
        
    def translate(self, word, context=None, pos_tag=None):
        """
        Translate word using a translation API
        Perform sentence contezt translation  on google web interface
        Perform word translation using Bing -> get all alternatives anc check for a mathc in the google translation, if match choose it as translation
        if not then choose the bing translation that best matches using POS tag?
        """
        #Get contextual translation from google translate
        par = {"text": word, "raw": "raw"}
        r = requests.post(self.translation_url, data=par)
        results = r.text
        translated_word = get_from_html_text(results, 'TRANSLATED_TEXT')
        
        #Perform lookup in the text file from the C# translator
        #if there is no match, take the best match from the bing file
#        print "Translated: ", word, " ->", translated_word
        return translated_word
    
def get_from_html_text(resultset, target):
    """
    Gets the value of a variable target from a html result set from a request.
    """
    index = resultset.find(target)+len(target)+2
    return resultset[index:index+140].split("'")[0].lower()
     
     
def perform_bing_sentiment_lexicon_lookup(tweets):
    """
    Performs sentiment lexicon lookup on the tweets, and stores it in the objects.
    """
    words = []
    for t in tweets:
        for phrase in t.tagged_words:
            for word in phrase:
                try:
                    if word["pos"] in TYPECRAFT_SENTIWORDNET:
                        words.append(word['word'])
                except KeyError:
                    continue 
                        
                
    lex = Lexicon(BingTranslater(words), SentiWordNetLexicon())
    words_with_sentimentvalues=[]#list of dicts
    print "Getting sentiment values"
    for t in tweets:
        sentiwords =[]
        sentiwords_with_values={}
        for phrase in t.tagged_words:
            for word in phrase:
                try:
                    if word["pos"] in TYPECRAFT_SENTIWORDNET:
                        sentiwords.append(word['word'])
                except KeyError:
                    continue
        for sentiword in sentiwords:
            sentivalues = lex.translate_and_get_lexicon_sentiment(sentiword)
            if sentivalues!=None:
                print "Adding sentivalues: ",sentivalues
                sentiwords_with_values[sentiword] = sentivalues
        words_with_sentimentvalues.append(sentiwords_with_values)
    
    return words_with_sentimentvalues
        
def perform_google_sentiment_lexicon_lookup(tweets):
    """
    Performs sentiment lexicon lookup on the tweets, and stores it in the objects.
    """
           
    lex = Lexicon(GoogleTranslater(), SentiWordNetLexicon())
    print "Getting sentiment values"
    tweet_sentiments = []
    for t in tweets:
        tweet_sentiments.append(lex.translate_sentence_and_get_lexicon_sentiment(t.text))
    
    print tweet_sentiments
    reduced_tweet_sentiments = []
    for sentiments in tweet_sentiments:
        polar_sum = sum([s[0] for s in sentiments])
        negative_sum = sum([s[1] for s in sentiments])
        objective_sum = sum([s[2] for s in sentiments])
        reduced_tweet_sentiments.append((polar_sum, negative_sum, objective_sum))
    print reduced_tweet_sentiments
    return reduced_tweet_sentiments

def tokenizer(sentence):
    """
    Tokenizes an english sentence.
    """
    words = []
    for phrase in sentence.split('.'):
        for piece in phrase.split(','):
            for word in piece.split(' '):
                words.append(word)
    return words
   
if __name__ == '__main__':
    #Insert all words to be translated into the googlebing translator in order to augment with Bing...
    lex = Lexicon(BingTranslater(), SentiWordNetLexicon())
    print lex.translate_and_get_lexicon_sentiment("good")
    
#    swn = SentiWordNetCorpusReader('SentiWordNet_3.0.0_20130122.txt')
#    for senti_synset in swn.all_senti_synsets():
#        print senti_synset.synset.name, senti_synset.pos_score, senti_synset.neg_score