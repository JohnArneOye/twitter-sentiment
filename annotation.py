'''
Created on 30. sep. 2014

@author: JohnArne
'''
import utils
import tweet
import os

def user_annotation():
    """
    Feed tweets to console one at a time, and ask user for sentiment annotation.
    """
    dataset = utils.select_dataset()
    text_tweets = utils.get_dataset(dataset)
    tweets = []
    for text_tweet in text_tweets:
        tweets.append(tweet.to_tweet(text_tweet))
    username = raw_input("Name? ... ")
    
    print "\n--------------\n"
    print "1: Negative sentiment (Negative opinion). 2: Neutral/objective sentiment (No opinion). 3: Positive sentiment (Positive opinion). x: Cancel sequence. 0: Go back to previous tweet. "
    print "\n--------------\n"
    
    annotated_to = 0
    i = 0
    while i < len(tweets):
#        tweets[i].text.encode('utf8')
        text = tweets[i].text
        text.encode('utf8')
        try:
            print unicode(text)
        except UnicodeEncodeError:
            print "Could not print tweet number "+str(i+1) +". Deleting tweet..."
            tweets.remove(tweets[i])
            continue
        
        userinput = raw_input("...")
        while not legal_input(userinput):
            userinput = raw_input("Unlawful input! Please re-introduce.")
        if userinput is '1':
            tweets[i].set_sentiment("negative")
        elif userinput is '2':
            tweets[i].set_sentiment("neutral")
        elif userinput is '3':
            tweets[i].set_sentiment("positive")
        elif userinput is '0':
            i = i-1
            continue
        elif userinput is 'x':
            break
        i = i+1
        
        
    #TODO: need to encode to utf when getting from dataset?!?!
    #Store the sentiment in file!
    tweetlines = []
    for t in tweets[:i]:
        if t.get_sentiment() is None:
            continue
        tweetlines.append(t.to_tsv())
    dir = username+"_annotated_data"
    if not os.path.exists(dir):
        os.makedirs(dir)
    utils.store_dataset(tweetlines, dir+dataset[4:])
    
    print "Domo arigato!" 
    
def legal_input(userinput):
    """
    Checks input and returns true if the input is legal. Legal input should be "1", "2", "3", or "x"
    """
    legal_inputs = ['1','2','3','0','x']
    
    if userinput in legal_inputs:
        return True
    return False