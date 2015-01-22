'''
Created on 4. jan. 2015

@author: JohnArne

-Ta en gruppe tweets.
-Prov a finne entitetene i hver enkelt tweet.
- kjor clustering pa tweets, eller pa bare entitetsnavn... grupper entitetene etter clusters og nominer den mest frekvente entiteten som overordnet navn
'''
import lexicon.pos_mappings
from lexicon import pos_mappings
from tweet import Tweet
import utils
from models.features import get_sentiment_values
import classifier
import pickle
from sklearn import metrics
import plotting
from sklearn.feature_extraction.text import CountVectorizer
import math


def perform_entity_extraction(tweets, sentimentvalues, breakword_min_freq=0.2, breakword_range=2, use_sentiment_values=False, use_pmi=False, vocabulary=None, cluster=False, use_minibatch=False, use_idf=False, use_hasher=False):
    """
    Takes in a list of correctly predicted subjective tweets and sentimentvalues, in addition to several optional parameters, and attempts entity extraction on all the tweeets.
    """
    print len(tweets)
    sub_clf = classifier.get_optimal_subjectivity_classifier()
    #Get all the correctly classified subjective tweets
    if use_pmi and vocabulary==None: vocabulary = create_vocabulary(tweets) 
    if use_sentiment_values:
        entities = find_entities(sub_clf, tweets, breakword_min_freq, breakword_range, use_pmi, vocabulary=vocabulary, sentimentvalues=sentimentvalues)
    else:
        entities = find_entities(sub_clf, tweets, breakword_min_freq, breakword_range, use_pmi, vocabulary=vocabulary)
    
    if cluster:
        #use clustering to group together tweets, 
        #then choose the entities with the greatest freqiencies within each cluster as the sentiment target for all in the cluster
        #but not if the target is already none...
        cluster_tweets(tweets, use_minibatch, use_idf, use_hasher)
    
    
    for i in xrange(len(entities)):
        entities[i] = entities[i][0] if len(entities[i])>0 else None
    print entities
    return entities

def find_entities(sub_clf, tweets, min_freq, breakword_range, use_pmi=False, vocabulary=None, sentimentvalues=None):
    """
    Takes in a subjectivity classifier and the tweets, and attempts to find the target of the classified sentiment.
    Return a textual description of the entity.
    """
    if sentimentvalues!=None:
        entities = [find_entity(sub_clf, t, min_freq, breakword_range, use_pmi, vocabulary=vocabulary, sentimentvalues=s) for t,s in zip(tweets,sentimentvalues)]
    else:
        entities = [find_entity(sub_clf, t, min_freq, breakword_range, use_pmi, vocabulary=vocabulary) for t in tweets]
    return entities
    
    
def find_entity(sub_clf, t, min_freq, breakword_range, use_pmi=False, vocabulary=None, sentimentvalues=None):
    """
    Attempts at identifying the entity of a single tweet, utilizing sentiment values if not none.
    """
    #get a list of possibilities for this tweet
    possibilities = get_possible_entities(t)
    if len(possibilities)<1:
        for hashtag in t.hashtags:
            if len(hashtag)>1:
                return [hashtag]
        return []
    if len(possibilities)==1:
        return possibilities
    
    #Get breakwords from breakdown classification
    breakwords = breakdown_classify(sub_clf, t)
    
    breakwords = cutoff_breakwords(breakwords, min_freq)
    #get sentimental words if given values
    sentimentwords = []
    if sentimentvalues!=None:
        sentimentwords = get_sentimentwords(sentimentvalues)
    
    #Perform an intersection of the breakwords and sentimental words
#    print "Text: ", t.text
#    print "Possible entities: ",possibilities
#    print "Hashtags: ",t.hashtags
#    print "Shifting words: ",breakwords
#    print "Sentimental words: ",sentimentwords
    sentiment_points = [val for val in sentimentwords if val in breakwords]
#    print "Intersection: ", sentiment_points
    if len(sentiment_points)<1: sentiment_points = list(set(breakwords + sentimentwords))
#    print "New intersection: ", sentiment_points
    
    possibilities = cutoff_possibilities(t.text.lower(), possibilities, sentiment_points, breakword_range)
#    print "Possibilities after cutoff: ", possibilities
#    raw_input("Continue?")

    if use_pmi:
        #Use PMI to disambiguate between possibilities
        pmi = []
        for p in possibilities:
            if p is None: continue
            for s in sentiment_points:
                if s is None: continue
                pmi.append([calculate_pmi(p,s,vocabulary), p])
        if len(pmi)>0:        
            possibilities = [max(pmi)[1]]
    
    if len(possibilities)>0:
        return possibilities 
    else:
        if len(t.hashtags)>0:
            for hashtag in t.hashtags:
                if len(hashtag)>1:
                    return [hashtag]
        return []
    
#    if len(possibilities)>0:
#        return t.hashtags[0] if len(t.hashtags)>0 else possibilities
#    else:
#        return t.hashtags
#    
    #decide entity from possibilities based on the sentiment points
    #calculate the "center" of the sentiment points
    #choose the entity which is closest to the center of the sentiment points
    #or choose the entity closest to the first sentiment points...
    
    
def calculate_pmi(entity, sentiword, vocabulary):
    """
    Calculates the pointwise mutual information between two given words.
    """
    unigrams_freq = float(sum(vocabulary[0].values()))
    prob_entity = vocabulary[0][entity] / unigrams_freq
    prob_sentiword = vocabulary[0][sentiword] / unigrams_freq
    try:
        prob_both = vocabulary[1][" ".join([unicode(entity),unicode(sentiword)])] / float(sum(vocabulary[1].values()))
    except KeyError:
        return 0.0
    except UnicodeDecodeError:
        print "UnicodeError"
        return 0.0
    return math.log(prob_both/float(prob_entity*prob_sentiword),2)
    
def create_vocabulary(tweets):
    """
    Creates a bigram + unigram vocabulary of the given tweet texts.
    """
    print "Creating vocabulary..."
    vocabulary = []
    unigrams_freq = {}
    bigrams_freq = {}
    texts= [t.text.lower() for t in tweets]
    for text in texts:
        for phrase in text.split('.'):
            phrase = phrase.replace(',',' ')
            unigrams = phrase.split(" ")
            unigrams = [u for u in unigrams if len(u)>1]
            extended_bigrams = [x+" "+y for x,y in zip(unigrams[0::2],unigrams[1::2])] + [x+" "+y for x,y in zip(unigrams[1::2],unigrams[2::2])] + [x+" "+y for x,y in zip(unigrams[0::2],unigrams[2::2])] + [x+" "+y for x,y in zip(unigrams[1::2],unigrams[3::2])]
            for unigram in unigrams:
                unigrams_freq[unigram]  = unigrams_freq.get(unigram, 0) + 1
            for bigram in extended_bigrams:
                bigrams_freq[bigram] = bigrams_freq.get(bigram, 0) + 1
    vocabulary = [unigrams_freq, bigrams_freq]
    return vocabulary

def is_entity(clf, t, entity, sentimentvalues=None):
    """
    Takes in a classifier, a tweet, and an entity, returns a binary value corresponding to whether each entity is the sentiment entity of each tweet.
    """
    
    return False
    
def get_possible_entities(t):
    """
    Takes in a tweet, and returns a list of the possible entities for that tweet.
    """
    possible_entities = []
    for phrase in t.tagged_words:
        for word in phrase:
            try:
                entity = word['word']
                if word['pos'] =="Np":
                    if len(entity)>1:
                        possible_entities.append(entity.lower())
            except KeyError:
                continue
    return possible_entities
        
def get_sentimentwords(sentimentvalues):
    """
    returns the words that contain sentimental value.
    """
    sentimentwords = []
    for word in sentimentvalues.keys():
        if sentimentvalues[word][0]>0 or sentimentvalues[word][1]>0:
            sentimentwords.append(word)
    return sentimentwords


def breakdown_classify(clf, t):
    """
    Classify substring permutations of the tweet in order to find a shifting point in the subjectivity classification
    """
    orig_class = clf.classify([t])
    breakwords = subclassify(t.text.lower(), clf, orig_class)
#    breakwords = []
#    print "Breakdown classification"
#    for substring_paths in substrings:
#        for substring_and_rmword in substring_paths:
#            print substring_and_rmword['substring'], " rm:",substring_and_rmword['removed_word']
#            #Classify each substring, append causal word when sentiment changes from original
#            new_class = clf.classify_text([" ".join(substring_and_rmword['substring'])])
#            print "New class: ",new_class
#            if new_class!=orig_class: 
#                breakwords.append(substring_and_rmword['removed_word'])
#                break
#    print "Original prediction: ",orig_class
    return breakwords
            


def subclassify(t, clf, orig):
    """
    Takes in a text, a classifier, and an original class. Returns all the break words where the class shifts. FIXXX!
    """
    phrases = t.split(",")
    words = []
    for phrase in phrases:
        words = words + phrase.split(" ")
    length = len(words)
    breakwords = []
    for i in xrange(length):
        breakwords.append(clf_sub(words[:i]+words[i+1:], words[i], clf, orig)) 

    return breakwords
    
def clf_sub(words, removed_word, clf, orig):
    """
    FIIIIX!!! Return on classification shift!!! yesaaaaa!
    """
    if len(words)==1: return removed_word if clf.classify_text([" ".join(words)])!=orig else None
    breakword = None
#    print " ".join(words), "Removed word: ", removed_word
    for i in xrange(len(words)-1):
        if clf.classify_text([" ".join(words)])!=orig:
#            print "Swithed class!"
            return removed_word
        return clf_sub(words[:i]+words[i+1:], words[i], clf, orig)
    return breakword
    
def cutoff_breakwords(breakwords, min_freq):
    """
    Cuts of breakwords below the given frequency. Returns a list of uniques, where the belowfreqs have been removed
    """
    breakword_freq = int(round(len(breakwords)*min_freq))
#    print "Breakwords before cutoff ",breakwords, min_freq
    frequencies = {}
    #remove breakwords with a lower frequency
    for word in breakwords:
        frequencies[word] = frequencies.get(word,0)+1
    uniquelist = list(set(breakwords))
    for key in frequencies:
        if frequencies[key]<breakword_freq:
            uniquelist.remove(key)
            
    return uniquelist

def cutoff_possibilities(text, possibilities, sentiment_points, breakword_range):
    """
    Removes the possible which are not within the breakword_range of any sentiment_points.
    """
    phrases = text.split(",")
    words = []
    sentiment_indexes = []
    for phrase in phrases:
        words = words + phrase.split(" ")
          
    for i in xrange(len(words)):
        if words[i] in sentiment_points:
            sentiment_indexes.append(i)      
          
    limited_possibilities = []
    for point in sentiment_indexes:
        min_breakoff = point-breakword_range
        max_breakoff = point+breakword_range 
        include_words = words[min_breakoff:max_breakoff+1]
        for possibility in possibilities:
            if possibility in include_words:
                limited_possibilities.append(possibility)
    
    return limited_possibilities

def get_hashtag_entities(tweets):
    """
    Returns the first hashtag of every tweet, else returns None
    """
    return [t.hashtags[0] if len(t.hashtags)>0 else None for t in tweets]
  
def reduce_entities(entities):
    """
    Reduce entities to binary so as to test with actual targets.
    """
    reduced = []
    for entity in entities:
        reduced.append(1 if entity in rosenborg_model else 0)
    return reduced

def get_scores(targets, predictions):
    accuracy = metrics.accuracy_score(targets, predictions)
    precision = metrics.precision_score(targets, predictions)
    recall = metrics.recall_score(targets, predictions)
    f1_score = metrics.f1_score(targets, predictions)
    return accuracy, precision, recall, f1_score

def create_model(text):
    model = [text]
    f = open(text+"_model", "wb")
    pickle.dump(model,f)
    f.close()
    
def append_to_model(name, text):
    model = pickle.load(name+"_model")
    model.append(text)
    model = list(set(model))
    f = open(name+"_model", "wb")
    pickle.dump(model, f)
    f.close()
    
def cluster_tweets(tweets, max_features, use_minibatch, use_idf, use_hasher):
    """
    Performs k-means clustering on tweets.
    """
    
    
    return None



def perform_and_test_extraction():
    datasetnr = 1
    tweets = utils.get_pickles(datasetnr)
    vocabulary = create_vocabulary(utils.get_all_pickles())
    
    sentimentvalues = get_sentiment_values(datasetnr)
    tweets, targets = utils.get_entity_test_and_targets()
    entities = perform_entity_extraction(tweets, sentimentvalues, breakword_range=3)
    hashtag_entities = get_hashtag_entities(tweets)
    
    pmi_entities = perform_entity_extraction(tweets, sentimentvalues, breakword_range=8, use_pmi=True, vocabulary=vocabulary)
    #TESTIFY!
    reduced_entities = reduce_entities(entities)
    reduced_hashtags = reduce_entities(hashtag_entities)
    reduced_pmis = reduce_entities(pmi_entities)
    
    data = {}
    accuracy, precision, recall, f1_score = get_scores(targets, reduced_entities)
    print "Entity Scores:  ", accuracy, precision, recall, f1_score
    data["Custom"] = [accuracy, precision, recall, f1_score] 
    accuracy, precision, recall, f1_score = get_scores(targets, reduced_hashtags)
    data["Hashtags"] = [accuracy, precision, recall, f1_score]
    print "Hashtag Scores:  ", accuracy, precision, recall, f1_score
    accuracy, precision, recall, f1_score = get_scores(targets, reduced_pmis)
    print "PMI Scores:  ", accuracy, precision, recall, f1_score
    data["Custom+PMI"] = [accuracy, precision, recall, f1_score]
    #send to plotting
    plotting.plot_entity_histogram(data, "entity_extraction")
    
    
rosenborg_model = ["rosenborg","rosenborgs","rosenborgms", "rbk","rbks","rosenborg2" ]
    
if __name__ == '__main__':
    #test substringify
#    substrings = subc(string)
#    print substrings
#    print len(substrings)
    #test breakdown clf
#    breakdown_classify("adwd", Tweet("12313", "johnaren", "jeg liker at"))
    perform_and_test_extraction()
    
    