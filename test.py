'''
Created on 24. nov. 2014

@author: JohnArne
'''
import utils
from models.nb import NB
from tweet import Tweet
import preprocessing

if __name__ == '__main__':
    tweets = utils.get_pickles()
    
    tweets, targets = utils.make_subjectivity_set_and_target(tweets)
    vect_options = {
          'ngram_range': (1,1),
          'sublinear_tf': True,
          'use_idf': True,
          'smooth_idf': True,
          'max_df': 0.5
        }
    nb = NB(tweets, targets, vect_options)
    nb.set_feature_set('A')
    nb.train_on_feature_set()
    tweet = Tweet("12.12.12 12:12", "johnarne", "Jeg liker Erna Solberg")
    tweet = preprocessing.preprocess_tweet(tweet)
    print nb.classify(tweet.text)