'''
Created on 27. nov. 2014

@author: JohnArne
'''
from sklearn.feature_extraction.text import CountVectorizer

def get_feature_set(tweet,featureset):
    if(featureset=='SA'):
        return get_feature_set_SA(tweet)
    elif(featureset=='SB'):            
        return get_feature_set_SB(tweet)
    elif(featureset=='SC'):            
        return get_feature_set_SC(tweet)
    elif(featureset=='PA'):              
        return get_feature_set_PA(tweet)
    elif(featureset=='PB'):            
        return get_feature_set_PB(tweet)
    elif(featureset=='PC'):            
        return get_feature_set_PC(tweet)
    

def get_feature_set_SA(tweet):
    """
    Retrieves a list of tweets objects and returns feature set SA, which is only text frequencies...
    """
    features= {}
    return features

def get_feature_set_SB(tweet):
    """
    Creates a dict with grammatical features to be included in classification. Returns it to the classification model.
    Features to be included: pos-tags, 
    """
    features= {
               'text_length': len(tweet.text)
               } #ADD ADDITIONAL FEATURES
    return features


def get_feature_set_SC(tweet):
    """
    Retrieves a list of tweets objects and returns feature set SC.
    """
    features= {
               'text_length': len(tweet.text)
               } #ADD ADDITIONAL FEATURES
    return features


def get_feature_set_PA(tweet):
    """
    Retrieves a list of tweets objects and returns feature set PA, which is noone... Only word tokens.
    """
    features= {}
    return features

def get_feature_set_PB(tweet):
    """
    Retrieves a list of tweets objects and returns feature set PB.
    """
    features= {
               'text_length': len(tweet.text)
               } #ADD ADDITIONAL FEATURES
    return features

def get_feature_set_PC(tweet):
    """
    Retrieves a list of tweets objects and returns feature set PC.
    """
    features= {
               'text_length': len(tweet.text)
               } #ADD ADDITIONAL FEATURES
    return features