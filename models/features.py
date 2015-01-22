'''
Created on 27. nov. 2014

@author: JohnArne
'''
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pickle

def get_feature_set(tweet,featureset,sentimentvalues):
    if(featureset=='SA'):
        return get_feature_set_SA(tweet)
    elif(featureset=='SB'):            
        return get_feature_set_SB(tweet)
    elif(featureset=='SC'):            
        return get_feature_set_SC(tweet,sentimentvalues)
    elif(featureset=='SC2'):            
        return get_feature_set_SC2(tweet,sentimentvalues)
    elif(featureset=='PA'):              
        return get_feature_set_PA(tweet)
    elif(featureset=='PB'):            
        return get_feature_set_PB(tweet)
    elif(featureset=='PC'):            
        return get_feature_set_PC(tweet,sentimentvalues)
    elif(featureset=='PC2'):            
        return get_feature_set_PC2(tweet,sentimentvalues)
    

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
    #pos-tag frequencies
#    print "Tagged words in tweet: ", tweet.tagged_words
    pos_tag_freq = {}
    additional_freq = {}
    for phrase in tweet.tagged_words:
        for word in phrase:
            try:
                tag = word['pos']
                pos_tag_freq[tag] = pos_tag_freq.get(tag, 0) + 1
#                if tag=='PRtinf':
#                    pos_tag_freq[tag] = pos_tag_freq.get(tag, 0) + 1
#                elif tag=='ADJS':
#                    pos_tag_freq[tag] = pos_tag_freq.get(tag, 0) + 1
#                elif tag=='ADJ':
#                    pos_tag_freq[tag] = pos_tag_freq.get(tag, 0) + 1
#                elif tag=='NP':
#                    pos_tag_freq[tag] = pos_tag_freq.get(tag, 0) + 1
#                elif tag=='DET':
#                    pos_tag_freq[tag] = pos_tag_freq.get(tag, 0) + 1
#                elif tag=='P':
#                    pos_tag_freq[tag] = pos_tag_freq.get(tag, 0) + 1
                if tag in ADJECTIVES:
                    additional_freq['adjectives'] = additional_freq.get(tag, 0) + 1
                elif tag in ADVERBS: 
                    additional_freq['adverbs'] = additional_freq.get(tag, 0) + 1
                elif tag in PRONOUNS:
                    additional_freq['pronoun'] = 1
            except KeyError:
                continue
#    print "Tag frequencies: ", pos_tag_freq
    for key in pos_tag_freq.keys():
        pos_tag_freq[key] = pos_tag_freq[key]*1.0
    #number of adjectives in sentence, number of adverbs in sentence(except ikke), pronoun in sentence(binary)    
    #Number of exclamation marks, number of emoticons,
    emoticons = tweet.nrof_happyemoticons+tweet.nrof_sademoticons
    if emoticons>0:
        additional_freq['emoticons'] = emoticons*1.0
    if tweet.nrof_exclamations>0:
        additional_freq['exclamations'] = tweet.nrof_exclamations*1.0
    
#    print "Additional frequencies: ", additional_freq
#    raw_input("Continue?")
    
    #Concatenate the dicts
    features= dict(pos_tag_freq.items() + additional_freq.items())
#    print "All features: ", features
#    raw_input("Continue?")
    return features


def get_feature_set_SC(tweet, sentimentvalues):
    """
    Retrieves a list of tweets objects and returns feature set SC.
    """
    pos_tag_freq = {}
    additional_freq = {}
    for phrase in tweet.tagged_words:
        for word in phrase:
            try:
                tag = word['pos']
                pos_tag_freq[tag] = pos_tag_freq.get(tag, 0) + 1
#                if tag=='PRtinf':
#                    pos_tag_freq[tag] = pos_tag_freq.get(tag, 0) + 1
#                elif tag=='ADJS':
#                    pos_tag_freq[tag] = pos_tag_freq.get(tag, 0) + 1
#                elif tag=='ADJ':
#                    pos_tag_freq[tag] = pos_tag_freq.get(tag, 0) + 1
#                elif tag=='NP':
#                    pos_tag_freq[tag] = pos_tag_freq.get(tag, 0) + 1
#                elif tag=='DET':
#                    pos_tag_freq[tag] = pos_tag_freq.get(tag, 0) + 1
#                elif tag=='P':
#                    pos_tag_freq[tag] = pos_tag_freq.get(tag, 0) + 1
                if tag in ADJECTIVES:
                    additional_freq['adjectives'] = additional_freq.get(tag, 0) + 1
                elif tag in ADVERBS: 
                    additional_freq['adverbs'] = additional_freq.get(tag, 0) + 1
                elif tag in PRONOUNS:
                    additional_freq['pronoun'] = 1
            except KeyError:
                continue
    for key in pos_tag_freq.keys():
        pos_tag_freq[key] = pos_tag_freq[key]*1.0
    #number of adjectives in sentence, number of adverbs in sentence(except ikke), pronoun in sentence(binary)    
    #Number of exclamation marks, number of emoticons,
    emoticons = tweet.nrof_happyemoticons+tweet.nrof_sademoticons
    if emoticons>0:
        additional_freq['emoticons'] = emoticons*1.0
    if tweet.nrof_exclamations>0:
        additional_freq['exclamations'] = tweet.nrof_exclamations*1.0
    
    #Add lexicon values
     #total subjectivity score from word polarities, total objectivity score, number of subjective words, number of objective words, e
    sub_score = 0.0
    obj_score = 0.0
    nrof_subwords = 0
    nrof_objwords = 0
    for word in sentimentvalues.keys():
        if sentimentvalues[word][0]>0:
            sub_score = sub_score + sentimentvalues[word][0]
            nrof_subwords = nrof_subwords + 1
        if sentimentvalues[word][1]>0:
            sub_score = sub_score + sentimentvalues[word][1]
            nrof_subwords = nrof_subwords + 1
        if sentimentvalues[word][2]>0:
            obj_score = obj_score + sentimentvalues[word][2]
            nrof_objwords = nrof_objwords + 1
    if sub_score>0:
        additional_freq["sub_score"] = sub_score+1.0
    if obj_score>0:
        additional_freq["obj_score"] = obj_score+1.0
    if nrof_subwords>0:
        additional_freq["subjective_words"] = nrof_subwords*1.0
    if nrof_objwords>0:
        additional_freq["objective_words"] = nrof_objwords*1.0
    
    #Concatenate the dicts
    features= dict(pos_tag_freq.items() + additional_freq.items())
    
    return features

def get_feature_set_SC2(tweet, sentimentvalues):
    """
    Retrieves a list of tweets objects and returns feature set SC.
    """
    pos_tag_freq = {}
    additional_freq = {}
    for phrase in tweet.tagged_words:
        for word in phrase:
            try:
                tag = word['pos']
                pos_tag_freq[tag] = pos_tag_freq.get(tag, 0) + 1
                if tag in ADJECTIVES:
                    additional_freq['adjectives'] = additional_freq.get(tag, 0) + 1
                elif tag in ADVERBS: 
                    additional_freq['adverbs'] = additional_freq.get(tag, 0) + 1
                elif tag in PRONOUNS:
                    additional_freq['pronoun'] = 1
            except KeyError:
                continue
    for key in pos_tag_freq.keys():
        pos_tag_freq[key] = pos_tag_freq[key]*1.0
    #number of adjectives in sentence, number of adverbs in sentence(except ikke), pronoun in sentence(binary)    
    #Number of exclamation marks, number of emoticons,
    emoticons = tweet.nrof_happyemoticons+tweet.nrof_sademoticons
    if emoticons>0:
        additional_freq['emoticons'] = emoticons*1.0
    if tweet.nrof_exclamations>0:
        additional_freq['exclamations'] = tweet.nrof_exclamations*1.0
    
    #Add lexicon values
     #total subjectivity score from word polarities, total objectivity score, number of subjective words, number of objective words, e
    sub_score = sentimentvalues[0]+sentimentvalues[1]
    obj_score = sentimentvalues[2]
    if sub_score>0:
        additional_freq["sub_score"] = sub_score+1.0
    if obj_score>0:
        additional_freq["obj_score"] = obj_score+1.0
    
    #Concatenate the dicts
    features= dict(pos_tag_freq.items() + additional_freq.items())
    
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
               'text_length': np.log(len(tweet.text))
               } #ADD ADDITIONAL FEATURES
    if tweet.nrof_sademoticons>0:
        features['sademoticons'] = tweet.nrof_sademoticons
    if tweet.nrof_happyemoticons>0:
        features['happyemoticons'] = tweet.nrof_happyemoticons
    
    return features

def get_feature_set_PC(tweet, sentimentvalues):
    """
    Retrieves a list of tweets objects and returns feature set PC.
    """
    features= {
               'text_length': np.log(len(tweet.text))
               } #ADD ADDITIONAL FEATURES
    if tweet.nrof_sademoticons>0:
        features['sademoticons'] = tweet.nrof_sademoticons
    if tweet.nrof_happyemoticons>0:
        features['happyemoticons'] = tweet.nrof_happyemoticons
    
    for phrase in tweet.tagged_words:
        for word in phrase:
            try:
                tag = word['pos']
                features[tag] = features.get(tag, 0) + 1
                if tag in ADJECTIVES:
                    features['adjectives'] = features.get(tag, 0) + 1
                elif tag in ADVERBS: 
                    features['adverbs'] = features.get(tag, 0) + 1
                elif tag in PRONOUNS:
                    features['pronoun'] = 1
            except KeyError:
                continue
    for key in features.keys():
        features[key] = features[key]*1.0
        
    #Add lexical features
    # total polarity score, number of positive words, number of negative words
    pos_score = 0
    neg_score = 0
    nrof_pos_words = 0
    nrof_neg_words = 0
    for word in sentimentvalues.keys():
        if sentimentvalues[word][0]>0:
            nrof_pos_words = nrof_pos_words + 1
            pos_score = pos_score + sentimentvalues[word][0]
        if sentimentvalues[word][1]>0:
            nrof_neg_words = nrof_neg_words + 1
            neg_score = neg_score + sentimentvalues[word][1]

    if neg_score>0:
        features['neg_score'] = neg_score+1.0
    if pos_score>0:
        features['pos_score'] = pos_score+1.0
    if nrof_pos_words>0:
        features['positive_words'] = nrof_pos_words*1.0
    if nrof_neg_words>0:
        features['negative_words'] = nrof_neg_words*1.0
    
    return features

def get_feature_set_PC2(tweet, sentimentvalues):
    """
    Retrieves a list of tweets objects and returns feature set PC.
    """
    features= {
               'text_length': np.log(len(tweet.text))
               } #ADD ADDITIONAL FEATURES
    if tweet.nrof_sademoticons>0:
        features['sademoticons'] = tweet.nrof_sademoticons
    if tweet.nrof_happyemoticons>0:
        features['happyemoticons'] = tweet.nrof_happyemoticons
    
    for phrase in tweet.tagged_words:
        for word in phrase:
            try:
                tag = word['pos']
                features[tag] = features.get(tag, 0) + 1
                if tag in ADJECTIVES:
                    features['adjectives'] = features.get(tag, 0) + 1
                elif tag in ADVERBS: 
                    features['adverbs'] = features.get(tag, 0) + 1
                elif tag in PRONOUNS:
                    features['pronoun'] = 1
            except KeyError:
                continue
    for key in features.keys():
        features[key] = features[key]*1.0
        
    #Add lexical features
    # total polarity score, number of positive words, number of negative words
    pos_score = sentimentvalues[0]
    neg_score = sentimentvalues[1]

    if pos_score>0:
        features['pos_score'] = pos_score+1.0
    if neg_score>0:
        features['neg_score'] = neg_score+1.0
    
    return features

def get_sentiment_values(setnr):
    """
    Gets the pickles of sentiment values
    """
    if setnr==None:
        setnr = int(raw_input("Get which pickle set? 0: RandomSet 1: RoseborgSet 2: ErnaSet 3: All three ..."))
        
    if setnr is 3:
        #fetch all sets and append them together
        tweets = []
        for pickleset in sentiment_pickles:
            tweets = tweets + pickle.load(open(pickleset, 'rb'))
        return tweets
    else:
        tweets = pickle.load(open(sentiment_pickles[setnr], 'rb'))
        return tweets
    
    return tweets

def get_google_sentiment_values(setnr):
    """
    Gets the pickles of sentiment values
    """
    if setnr==None:
        setnr = int(raw_input("Get which pickle set? 0: RandomSet 1: RoseborgSet 2: ErnaSet 3: All three ..."))
        
    if setnr is 3:
        #fetch all sets and append them together
        tweets = []
        for pickleset in google_sentiment_pickles:
            tweets = tweets + pickle.load(open(pickleset, 'rb'))
        return tweets
    else:
        tweets = pickle.load(open(google_sentiment_pickles[setnr], 'rb'))
        return tweets
    
    return tweets

sentiment_pickles = ['models/sentimentvalues_random_dataset',
           'models/sentimentvalues_rosenborg_dataset',
           'models/sentimentvalues_erna_dataset']
google_sentiment_pickles = ['models/google_sentimentvalues_random_dataset',
           'models/google_sentimentvalues_rosenborg_dataset',
           'models/google_sentimentvalues_erna_dataset']

ADJECTIVES = ['ADJ','ADJC','ADJS']
ADVERBS = ['ADV','ADVm','ADVneg','ADVplc','ADVtemp']
PRONOUNS = ['PN','PNabs','PNana','PNdem','PNposs','PNrefl','PNrel']
NOUNS = ['CN','N','Nbare','Ncomm','NDV','NFEM','NMASC','NNEUT','NNO','Np','Nrel','Nspat']