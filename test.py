'''
Created on 24. nov. 2014
Methods for performing test on various classificatino schemes and storing the results.
@author: JohnArne
'''
import utils
from lexicon import lexicon
from models.nb import NB
from models.svm import SVM
from models.me import ME
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from tweet import Tweet
import plotting
import preprocessing
import models.features as feat_utils

    
def train_and_test_subjectivity_and_polarity():
    datasetnr = 3
    tweets = utils.get_pickles(datasetnr)
    sentimentvalues = feat_utils.get_sentiment_values(datasetnr)
    tweets = preprocessing.remove_link_classes(tweets)
    tweets = preprocessing.lower_case(tweets)
    tweets = preprocessing.remove_specialchars_round2(tweets)
    
#    train_subjectivity_and_test_on_feature_set(tweets, 'SA', sentimentvalues)
#    train_subjectivity_and_test_on_feature_set(tweets, 'SB', sentimentvalues)
#    train_subjectivity_and_test_on_feature_set(tweets, 'SC', sentimentvalues)
    
    train_polarity_and_test_on_feature_set(tweets, 'PA', sentimentvalues)
    train_polarity_and_test_on_feature_set(tweets, 'PB', sentimentvalues)
    train_polarity_and_test_on_feature_set(tweets, 'PC', sentimentvalues)

def train_subjectivity_and_test_on_feature_set(tweets, feature_set, sentimentvalues):
    """
    Performs training and testing with a given feature set key
    """
    train_tweets, train_targets, test_tweets, test_targets, train_sentimentvalues, test_sentimentvalues = utils.make_subjectivity_train_and_test_and_targets(tweets,sentimentvalues)
#    for tweet, target in zip(tweets,targets):
#        try:
#            print unicode(tweet.text), " ", target
#        except UnicodeEncodeError:
#            print tweet.text.encode('utf8'), " ", target
#        except UnicodeDecodeError:
#            print tweet.text, " ", target
    
    #TRAINING NB
    vect_options = {
          'ngram_range': (1,1),
          'max_df': 0.5
        }
    tfidf_options = {
         'sublinear_tf': False,
          'use_idf': True,
          'smooth_idf': True,
                     }
    print "Training NB subjectivity on dataset of length ", len(train_tweets)
    clf = NB(train_tweets, train_targets, vect_options, tfidf_options)
    clf.set_feature_set(feature_set, train_sentimentvalues)
    clf.train_on_feature_set()
    print "Testing..."
    nb_accuracy, nb_precision, nb_recall, nb_f1_score = clf.test_and_return_results(test_tweets, test_targets, test_sentimentvalues)
    
    #TRAINING SVM
    vect_options = {
          'ngram_range': (1,3),
          'max_df': 0.5

        }
    tfidf_options = {
         'sublinear_tf': True,
          'use_idf': True,
          'smooth_idf': True,
                     }
    print "Training SVM subjectivity on dataset of length ", len(train_tweets)
    clf = SVM(train_tweets, train_targets, vect_options, tfidf_options)
    clf.set_feature_set(feature_set, train_sentimentvalues)
    clf.train_on_feature_set()

    print "Testing..."
    svm_accuracy, svm_precision, svm_recall, svm_f1_score = clf.test_and_return_results(test_tweets, test_targets, test_sentimentvalues)
    
    #TRAINING MAXENT
    vect_options = {
      'ngram_range': (1,2),
          'max_df': 0.5
    }
    tfidf_options = {
                     'sublinear_tf': True,
                      'use_idf': True,
                      'smooth_idf': True,
                     }
    print "Training MaxEnt subjectivity on dataset of length ", len(train_tweets)
    clf = ME(train_tweets, train_targets, vect_options, tfidf_options)
    clf.set_feature_set(feature_set, train_sentimentvalues)
    clf.train_on_feature_set()

    print "Testing..."
    me_accuracy, me_precision, me_recall, me_f1_score = clf.test_and_return_results(test_tweets, test_targets, test_sentimentvalues)
    
    
    data = {'Naive Bayes': [nb_accuracy, nb_precision, nb_recall, nb_f1_score],
            'SVM': [svm_accuracy, svm_precision, svm_recall, svm_f1_score],
            'Maximum Entropy': [me_accuracy, me_precision, me_recall, me_f1_score]}
    plotting.plot_performance_histogram(data, "subjectivity_"+feature_set)

def train_polarity_and_test_on_feature_set(tweets, feature_set, sentimentvalues):
    """
    Performs training and testing with a given feature set key
    """
    train_tweets, train_targets, test_tweets, test_targets, train_sentimentvalues, test_sentimentvalues = utils.make_polarity_train_and_test_and_targets(tweets,sentimentvalues)
#    for tweet, target in zip(tweets,targets):
#        try:
#            print unicode(tweet.text), " ", target
#        except UnicodeEncodeError:
#            print tweet.text.encode('utf8'), " ", target
#        except UnicodeDecodeError:
#            print tweet.text, " ", target
    
    #TRAINING NB
    vect_options = {
          'ngram_range': (1,1),
          'max_df': 0.5
        }
    tfidf_options = {
          'sublinear_tf': True,
          'use_idf': True,
          'smooth_idf': True,
          }
    print "Training NB polarity on dataset of length ", len(train_tweets)
    clf = NB(train_tweets, train_targets, vect_options, tfidf_options)
    clf.set_feature_set(feature_set, train_sentimentvalues)
    clf.train_on_feature_set()
    print "Testing..."
    nb_accuracy, nb_precision, nb_recall, nb_f1_score = clf.test_and_return_results(test_tweets, test_targets, test_sentimentvalues)
    
    #TRAINING SVM
    vect_options = {
          'ngram_range': (1,1),
          'max_df': 0.5
        }
    tfidf_options= {
          'sublinear_tf': True,
          'use_idf': True,
          'smooth_idf': True,
          }
    print "Training SVM polarity on dataset of length ", len(train_tweets)
    clf = SVM(train_tweets, train_targets, vect_options, tfidf_options)
    clf.set_feature_set(feature_set, train_sentimentvalues)
    clf.train_on_feature_set()

    print "Testing..."
    svm_accuracy, svm_precision, svm_recall, svm_f1_score = clf.test_and_return_results(test_tweets, test_targets, test_sentimentvalues)
    
    #TRAINING MAXENT
    vect_options = {
      'ngram_range': (1,1),
      'max_df': 0.5
    }
    tfidf_options = {
      'sublinear_tf': True,
      'use_idf': True,
      'smooth_idf': True,
      }
    print "Training MaxEnt polarity on dataset of length ", len(train_tweets)
    clf = ME(train_tweets, train_targets, vect_options, tfidf_options)
    clf.set_feature_set(feature_set, train_sentimentvalues)
    clf.train_on_feature_set()

    print "Testing..."
    me_accuracy, me_precision, me_recall, me_f1_score = clf.test_and_return_results(test_tweets, test_targets, test_sentimentvalues)
    
    
    data = {'Naive Bayes': [nb_accuracy, nb_precision, nb_recall, nb_f1_score],
            'SVM': [svm_accuracy, svm_precision, svm_recall, svm_f1_score],
            'Maximum Entropy': [me_accuracy, me_precision, me_recall, me_f1_score]}
    plotting.plot_performance_histogram(data, "polarity_"+feature_set)


def perform_grid_search_on_featureset_SA_and_PA():
    datasetnr = 3
    tweets = utils.get_pickles(datasetnr)
    sentimentvalues = feat_utils.get_sentiment_values(datasetnr)
    tweets = preprocessing.remove_link_classes(tweets)
    tweets = preprocessing.lower_case(tweets)
    tweets = preprocessing.remove_specialchars_round2(tweets)
    
    train_tweets, train_targets, test_tweets, test_targets, train_sentimentvalues, test_sentimentvalues = utils.make_subjectivity_train_and_test_and_targets(tweets,sentimentvalues)
    
    clf = SVM(train_tweets, train_targets, None)
    clf.set_feature_set('SA', None)
    clf.grid_search_on_text_features(file_postfix='subjectivity')
    clf = NB(train_tweets, train_targets, None)
    clf.set_feature_set('SA', None)
    clf.grid_search_on_text_features(file_postfix='subjectivity')
    clf = ME(train_tweets, train_targets, None)
    clf.set_feature_set('SA', None)
    clf.grid_search_on_text_features(file_postfix='subjectivity')
    
    train_tweets, train_targets, test_tweets, test_targets, train_sentimentvalues, test_sentimentvalues = utils.make_polarity_train_and_test_and_targets(tweets,sentimentvalues)
    
    clf = SVM(train_tweets, train_targets, None)
    clf.set_feature_set('PA', None)
    clf.grid_search_on_text_features(file_postfix='polarity')
    clf = NB(train_tweets, train_targets, None)
    clf.set_feature_set('PA', None)
    clf.grid_search_on_text_features(file_postfix='polarity')
    clf = ME(train_tweets, train_targets, None)
    clf.set_feature_set('PA', None)
    clf.grid_search_on_text_features(file_postfix='polarity')
    
if __name__ == '__main__':
    datasetnr = 3
    tweets = utils.get_pickles(datasetnr)
    sentimentvalues = feat_utils.get_sentiment_values(datasetnr)
    tweets = preprocessing.remove_link_classes(tweets)
    tweets = preprocessing.lower_case(tweets)
    tweets = preprocessing.remove_specialchars_round2(tweets)
    
#    train_subjectivity_and_test_on_feature_set(tweets, 'SA', datasetnr)
#    train_subjectivity_and_test_on_feature_set(tweets, 'SB', datasetnr)
    train_subjectivity_and_test_on_feature_set(tweets, 'SC', sentimentvalues)
    
#    train_polarity_and_test_on_feature_set(tweets, 'PA', datasetnr)
#    train_polarity_and_test_on_feature_set(tweets, 'PB', datasetnr)
    train_polarity_and_test_on_feature_set(tweets, 'PC', sentimentvalues)