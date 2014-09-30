'''
Created on 30. sep. 2014

@author: JohnArne
'''
import utils
import tweet

def user_annotation():
    """
    Feed tweets to console one at a time, and ask user for sentiment annotation.
    """
    dataset = utils.select_dataset()
    text_tweets = utils.get_dataset(dataset)
    tweets = []
    for text_tweet in text_tweets:
        tweets.append(tweet.to_tweet(text_tweet))
    
    print "1: Negative sentiment (Negative opinion). 2: Neutral/objective sentiment (No opinion). 3: Positive sentiment (Positive opinion). x: Cancel sequence. 0: Go back to previous tweet. "
    
    for i in range(0, len(tweets)):
        print str(tweets[i])
        userinput = raw_input("...")
        while not legal_input(userinput):
                userinput = raw_input("Unlawful input! Please re-introduce.")
        if userinput is 1:
            tweet.polarity = 0
            tweet.subjectivity = 1
        elif userinput is 2:
            tweet.polarity = 0
            tweet.subjectivity = 0
        elif userinput is 3:
            tweet.polarity = 1
            tweet.subjectivity = 1
        elif userinput is 0:
            i = i-1
            continue
        elif userinput is 'x':
            break
        
    #Store the sentiment in file!
    
    
    print "Domo arigato!" 
    
def legal_input(userinput):
    """
    Checks input and returns true if the input is legal. Legal input should be "1", "2", "3", or "x"
    """
    return False