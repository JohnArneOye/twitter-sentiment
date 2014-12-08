'''
Created on 24. nov. 2014

@author: JohnArne
'''
import utils
from models.nb import NB
from tweet import Tweet
import preprocessing

if __name__ == '__main__':
    nb = NB(utils.get_pickles())
    nb.set_feature_set('A')
    nb.train_on_feature_set()
    tweet = Tweet("12.12.12 12:12", "johnarne", "Jeg liker Erna Solberg")
    tweet = preprocessing.preprocess_tweet(Tweet())
    nb.classify(tweet)