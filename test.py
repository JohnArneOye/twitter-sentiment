'''
Created on 24. nov. 2014

@author: JohnArne
'''
import utils
from models.nb import NB
from models.svm import SVM
from models.me import ME
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from tweet import Tweet
import plotting
import preprocessing

    
def train_subjectivity_and_test_on_feature_set(tweets, feature_set):
    """
    Performs training and testing with a given feature set key
    """
    train_tweets, train_targets, test_tweets, test_targets = utils.make_subjectivity_train_and_test_and_targets(tweets)
#    for tweet, target in zip(tweets,targets):
#        try:
#            print unicode(tweet.text), " ", target
#        except UnicodeEncodeError:
#            print tweet.text.encode('utf8'), " ", target
#        except UnicodeDecodeError:
#            print tweet.text, " ", target
    
    #TRAINING NB
    vect_options = {
          'ngram_range': (1,3),
#          'sublinear_tf': True,
#          'use_idf': True,
#          'smooth_idf': True,
#          'max_df': 0.5
        }
    print "Training NB subjectivity on dataset of length ", len(train_tweets)
    clf = NB(train_tweets, train_targets, vect_options)
    clf.set_feature_set(feature_set)
    clf.train_on_feature_set()
    print "Testing..."
    nb_accuracy, nb_precision, nb_recall, nb_f1_score = clf.test_and_return_results(test_tweets, test_targets)
    
    #TRAINING SVM
    vect_options = {
          'ngram_range': (1,3),
#          'sublinear_tf': True,
#          'use_idf': True,
#          'smooth_idf': True,
#          'max_df': 0.5
        }
    print "Training SVM subjectivity on dataset of length ", len(train_tweets)
    clf = SVM(train_tweets, train_targets, vect_options)
    clf.set_feature_set(feature_set)
    clf.train_on_feature_set()

    print "Testing..."
    svm_accuracy, svm_precision, svm_recall, svm_f1_score = clf.test_and_return_results(test_tweets, test_targets)
    
    #TRAINING MAXENT
    vect_options = {
      'ngram_range': (1,3),
#      'sublinear_tf': True,
#      'use_idf': True,
#      'smooth_idf': True,
#      'max_df': 0.5
    }
    print "Training MaxEnt subjectivity on dataset of length ", len(train_tweets)
    clf = ME(train_tweets, train_targets, vect_options)
    clf.set_feature_set(feature_set)
    clf.train_on_feature_set()

    print "Testing..."
    me_accuracy, me_precision, me_recall, me_f1_score = clf.test_and_return_results(test_tweets, test_targets)
    
    
    data = {'Naive Bayes': [nb_accuracy, nb_precision, nb_recall, nb_f1_score],
            'SVM': [svm_accuracy, svm_precision, svm_recall, svm_f1_score],
            'Maximum Entropy': [me_accuracy, me_precision, me_recall, me_f1_score]}
    plotting.plot_performance_histogram(data, "subjectivity_"+feature_set)

def train_polarity_and_test_on_feature_set(tweets, feature_set):
    """
    Performs training and testing with a given feature set key
    """
    train_tweets, train_targets, test_tweets, test_targets = utils.make_polarity_train_and_test_and_targets(tweets)
#    for tweet, target in zip(tweets,targets):
#        try:
#            print unicode(tweet.text), " ", target
#        except UnicodeEncodeError:
#            print tweet.text.encode('utf8'), " ", target
#        except UnicodeDecodeError:
#            print tweet.text, " ", target
    
    #TRAINING NB
    vect_options = {
          'ngram_range': (1,3),
#          'sublinear_tf': True,
#          'use_idf': True,
#          'smooth_idf': True,
#          'max_df': 0.5
        }
    print "Training NB polarity on dataset of length ", len(train_tweets)
    clf = NB(train_tweets, train_targets, vect_options)
    clf.set_feature_set(feature_set)
    clf.train_on_feature_set()
    print "Testing..."
    nb_accuracy, nb_precision, nb_recall, nb_f1_score = clf.test_and_return_results(test_tweets, test_targets)
    
    #TRAINING SVM
    vect_options = {
          'ngram_range': (1,3),
#          'sublinear_tf': True,
#          'use_idf': True,
#          'smooth_idf': True,
#          'max_df': 0.5
        }
    print "Training SVM polarity on dataset of length ", len(train_tweets)
    clf = SVM(train_tweets, train_targets, vect_options)
    clf.set_feature_set(feature_set)
    clf.train_on_feature_set()

    print "Testing..."
    svm_accuracy, svm_precision, svm_recall, svm_f1_score = clf.test_and_return_results(test_tweets, test_targets)
    
    #TRAINING MAXENT
    vect_options = {
      'ngram_range': (1,3),
#      'sublinear_tf': True,
#      'use_idf': True,
#      'smooth_idf': True,
#      'max_df': 0.5
    }
    print "Training MaxEnt polarity on dataset of length ", len(train_tweets)
    clf = ME(train_tweets, train_targets, vect_options)
    clf.set_feature_set(feature_set)
    clf.train_on_feature_set()

    print "Testing..."
    me_accuracy, me_precision, me_recall, me_f1_score = clf.test_and_return_results(test_tweets, test_targets)
    
    
    data = {'Naive Bayes': [nb_accuracy, nb_precision, nb_recall, nb_f1_score],
            'SVM': [svm_accuracy, svm_precision, svm_recall, svm_f1_score],
            'Maximum Entropy': [me_accuracy, me_precision, me_recall, me_f1_score]}
    plotting.plot_performance_histogram(data, "polarity_"+feature_set)

    
if __name__ == '__main__':
    tweets = utils.get_pickles()
    tweets = preprocessing.remove_link_classes(tweets)
    tweets = preprocessing.lower_case(tweets)
    tweets = preprocessing.remove_specialchars_round2(tweets)
    
    train_subjectivity_and_test_on_feature_set(tweets, 'SA')
    train_subjectivity_and_test_on_feature_set(tweets, 'SB')
    train_subjectivity_and_test_on_feature_set(tweets, 'SC')
    
    train_polarity_and_test_on_feature_set(tweets, 'PA')
    train_polarity_and_test_on_feature_set(tweets, 'PB')
    train_polarity_and_test_on_feature_set(tweets, 'PC')