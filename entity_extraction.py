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

def perform_entity_extraction():
    datasetnr = 1
    tweets = utils.get_pickles(datasetnr)
    sentimentvalues = get_sentiment_values(datasetnr)
    sub_clf = classifier.get_optimal_subjectivity_classifier()
    #Get all the correctly classified subjective tweets
    correctly_subjective_tweets = sub_clf.get_correctly_classified_tweets([t for t in tweets if t.subjectivity==1])
    
    raw_input("Contine?")
    
    entities = find_entities(sub_clf, correctly_subjective_tweets, sentimentvalues)
    
    

def find_entities(sub_clf, tweets, sentimentvalues=None):
    """
    Takes in a subjectivity classifier and the tweets, and attempts to find the target of the classified sentiment.
    Return a textual description of the entity.
    """
    if sentimentvalues!=None:
        entities = [find_entity(sub_clf, t, s) for t,s in zip(tweets,sentimentvalues)]
    else:
        entities = [find_entity(sub_clf, t) for t in tweets]
    return entities
    
    
def find_entity(sub_clf, t, sentimentvalues=None):
    """
    Attempts at identifying the entity of a single tweet, utilizing sentiment values if not none.
    """
    #get a list of possibilities for this tweet
    possibilities = get_possible_entities(t)
    if len(possibilities)<1:
        return None
    if len(possibilities)==1:
        return possibilities[0]
    
    #Get breakwords from breakdown classification
    breakwords = breakdown_classify(sub_clf, t)
    
    #get sentimental words if given values
    sentimentwords = []
    if sentimentvalues!=None:
        sentimentwords = get_sentimentwords(sentimentvalues)
    
    print "Text: ", t.text
    print "Possible entities: ",possibilities
    
    print "Shifting words: ",breakwords
    print "Sentimental words: ",sentimentwords
    #Perform an intersection of the breakwords and sentimental words
    sentiment_points = [val for val in sentimentwords if val in breakwords]
    print "Intersection: ", sentiment_points
    if len(sentiment_points)<1: sentiment_points = list(set(breakwords + sentimentwords))
    print "New intersection: ", sentiment_points
    raw_input("Continue?")
    
    #decide entity from possibilities based on the sentiment points
    #calculate the "center" of the sentiment points
    #choose the entity which is closest to the center of the sentiment points
    #or choose the entity closest to the first sentiment points...
    
    
    
    
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
                if word['pos'] in pos_mappings.NOUNS or word['pos'] in pos_mappings.PRONOUNS:
                    possible_entities.append(word['word'].lower())
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
    return list(set(breakwords))
            


def subclassify(t, clf, orig):
    """
    Takes in a text, a classifier, and an original class. Returns all the break words where the class shifts. FIXXX!
    """
    words = t.split(' ')
    length = len(words)
    substrings = []
    for i in xrange(length):
        substrings = substrings + create_subdicts(words[:i]+words[i+1:], words[i]) 

    return substrings
    
def create_subdicts(words, removed_word):
    """
    FIIIIX!!! Return on classification shift!!! yesaaaaa!
    """
    if len(words)==1: return [{'substring': words, 'removed_word': removed_word}]
    substrings = []
    for i in xrange(len(words)-1):
        substrings = substrings + [ {'substring': words, 'removed_word': removed_word} ]
        substrings = substrings + create_subdicts(words[:i]+words[i+1:], words[i])
    return substrings
    

if __name__ == '__main__':
    #test substringify
    string = "jeg liker at erna solberg er  kul hun hopper opp og ned og er liksom bare helt kul der det er kult way what liksom"
#    substrings = subc(string)
#    print substrings
#    print len(substrings)
    #test breakdown clf
#    breakdown_classify("adwd", Tweet("12313", "johnaren", "jeg liker at"))
    perform_entity_extraction()
    
    