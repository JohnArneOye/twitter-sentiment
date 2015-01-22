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
import pickle
import classifier
import tweet
import entity_extraction
from entity_extraction import cutoff_breakwords
    
    
def train_and_test_subjectivity_and_polarity():
    datasetnr = 3
    tweets = utils.get_pickles(datasetnr)
    sentimentvalues = feat_utils.get_sentiment_values(datasetnr)
    tweets = preprocessing.remove_link_classes(tweets)
    tweets = preprocessing.lower_case(tweets)
    tweets = preprocessing.remove_specialchars_round2(tweets)
    
#    train_subjectivity_and_test_on_feature_set(tweets, 'SA', sentimentvalues)
    train_subjectivity_and_test_on_feature_set(tweets, 'SB', sentimentvalues)
    train_subjectivity_and_test_on_feature_set(tweets, 'SC', sentimentvalues)
#    google_sentimentvalues = feat_utils.get_google_sentiment_values(datasetnr)
#    train_subjectivity_and_test_on_feature_set(tweets, 'SC2', google_sentimentvalues)
    
#    train_polarity_and_test_on_feature_set(tweets, 'PA', sentimentvalues)
#    train_polarity_and_test_on_feature_set(tweets, 'PB', sentimentvalues)
#    train_polarity_and_test_on_feature_set(tweets, 'PC', sentimentvalues)
#    google_sentimentvalues = feat_utils.get_google_sentiment_values(datasetnr)
#    train_polarity_and_test_on_feature_set(tweets, 'PC2', google_sentimentvalues)

def train_subjectivity_and_test_on_feature_set(tweets, feature_set, sentimentvalues, reduce_dataset=1):
    """
    Performs training and testing with a given feature set key
    """
    kfolds = range(0,10)
    nbaccuracy_avgs = []
    nbprecision_avgs = []
    nbrecall_avgs = []
    nbf1_avgs = []
    svmaccuracy_avgs = []
    svmprecision_avgs = []
    svmrecall_avgs = []
    svmf1_avgs = []
    meaccuracy_avgs = []
    meprecision_avgs = []
    merecall_avgs = []
    mef1_avgs = []
    vect_options = {
          'ngram_range': (1,1),
          'max_df': 0.5
        }
    tfidf_options = {
         'sublinear_tf': False,
          'use_idf': True,
          'smooth_idf': True,
                     }
    for kfoldcounter in kfolds:
        print "--------------------------KFOLD NR ",kfoldcounter,"----------------------------------" 
        train_tweets, train_targets, test_tweets, test_targets, train_sentimentvalues, test_sentimentvalues = utils.make_subjectivity_train_and_test_and_targets(tweets,sentimentvalues,splitvalue=kfoldcounter*0.1,reduce_dataset=reduce_dataset)      
        #TRAINING NB
        print "Training NB subjectivity on dataset of length ", len(train_tweets)
        clf = NB(train_tweets, train_targets, vect_options, tfidf_options)
        clf.set_feature_set(feature_set, train_sentimentvalues)
        clf.train_on_feature_set()
        print "Testing..."
        nb_accuracy, nb_precision, nb_recall, nb_f1_score = clf.test_and_return_results(test_tweets, test_targets, test_sentimentvalues)
        nbaccuracy_avgs.append(nb_accuracy)
        nbprecision_avgs.append(nb_precision)
        nbrecall_avgs.append(nb_recall)
        nbf1_avgs.append(nb_f1_score)
        
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
        svmaccuracy_avgs.append(svm_accuracy)
        svmprecision_avgs.append(svm_precision)
        svmrecall_avgs.append(svm_recall)
        svmf1_avgs.append(svm_f1_score)
        
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
        meaccuracy_avgs.append(me_accuracy)
        meprecision_avgs.append(me_precision)
        merecall_avgs.append(me_recall)
        mef1_avgs.append(me_f1_score)
    
    
    print "Averages"
    nb_accuracy = reduce(lambda x,y: x+y,nbaccuracy_avgs)/len(nbaccuracy_avgs)
    nb_precision = reduce(lambda x,y: x+y,nbprecision_avgs)/len(nbprecision_avgs)
    nb_recall = reduce(lambda x,y: x+y,nbrecall_avgs)/len(nbrecall_avgs)
    nb_f1_score = reduce(lambda x,y: x+y,nbf1_avgs)/len(nbf1_avgs)
    svm_accuracy = reduce(lambda x,y: x+y,svmaccuracy_avgs)/len(svmaccuracy_avgs)
    svm_precision = reduce(lambda x,y: x+y,svmprecision_avgs)/len(svmprecision_avgs)
    svm_recall = reduce(lambda x,y: x+y,svmrecall_avgs)/len(svmrecall_avgs)
    svm_f1_score = reduce(lambda x,y: x+y,svmf1_avgs)/len(svmf1_avgs)
    me_accuracy = reduce(lambda x,y: x+y,meaccuracy_avgs)/len(meaccuracy_avgs)
    me_precision = reduce(lambda x,y: x+y,meprecision_avgs)/len(meprecision_avgs)
    me_recall = reduce(lambda x,y: x+y,merecall_avgs)/len(merecall_avgs)
    me_f1_score = reduce(lambda x,y: x+y,mef1_avgs)/len(mef1_avgs)
    
    data = {'Naive Bayes': [nb_accuracy, nb_precision, nb_recall, nb_f1_score],
            'SVM': [svm_accuracy, svm_precision, svm_recall, svm_f1_score],
            'Maximum Entropy': [me_accuracy, me_precision, me_recall, me_f1_score]}
    plotting.plot_performance_histogram(data, "subjectivity_"+feature_set)
    return data

def train_polarity_and_test_on_feature_set(tweets, feature_set, sentimentvalues, reduce_dataset=1):
    """
    Performs training and testing with a given feature set key
    """
    kfolds = range(0,10)
    nbaccuracy_avgs = []
    nbprecision_avgs = []
    nbrecall_avgs = []
    nbf1_avgs = []
    svmaccuracy_avgs = []
    svmprecision_avgs = []
    svmrecall_avgs = []
    svmf1_avgs = []
    meaccuracy_avgs = []
    meprecision_avgs = []
    merecall_avgs = []
    mef1_avgs = []
    for kfoldcounter in kfolds:
        print "--------------------------KFOLD NR ",kfoldcounter,"----------------------------------" 
        train_tweets, train_targets, test_tweets, test_targets, train_sentimentvalues, test_sentimentvalues = utils.make_polarity_train_and_test_and_targets(tweets,sentimentvalues, splitvalue=kfoldcounter*0.1, reduce_dataset=reduce_dataset)
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
        print "Training NB polarity with feature set ",feature_set
        clf = NB(train_tweets, train_targets, vect_options, tfidf_options)
        clf.set_feature_set(feature_set, train_sentimentvalues)
        clf.train_on_feature_set()
        print "Testing..."
        nb_accuracy, nb_precision, nb_recall, nb_f1_score = clf.test_and_return_results(test_tweets, test_targets, test_sentimentvalues)
        nbaccuracy_avgs.append(nb_accuracy)
        nbprecision_avgs.append(nb_precision)
        nbrecall_avgs.append(nb_recall)
        nbf1_avgs.append(nb_f1_score)
        
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
        svmaccuracy_avgs.append(svm_accuracy)
        svmprecision_avgs.append(svm_precision)
        svmrecall_avgs.append(svm_recall)
        svmf1_avgs.append(svm_f1_score)
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
        meaccuracy_avgs.append(me_accuracy)
        meprecision_avgs.append(me_precision)
        merecall_avgs.append(me_recall)
        mef1_avgs.append(me_f1_score)
        
    print "Averages"
    nb_accuracy = reduce(lambda x,y: x+y,nbaccuracy_avgs)/len(nbaccuracy_avgs)
    nb_precision = reduce(lambda x,y: x+y,nbprecision_avgs)/len(nbprecision_avgs)
    nb_recall = reduce(lambda x,y: x+y,nbrecall_avgs)/len(nbrecall_avgs)
    nb_f1_score = reduce(lambda x,y: x+y,nbf1_avgs)/len(nbf1_avgs)
    svm_accuracy = reduce(lambda x,y: x+y,svmaccuracy_avgs)/len(svmaccuracy_avgs)
    svm_precision = reduce(lambda x,y: x+y,svmprecision_avgs)/len(svmprecision_avgs)
    svm_recall = reduce(lambda x,y: x+y,svmrecall_avgs)/len(svmrecall_avgs)
    svm_f1_score = reduce(lambda x,y: x+y,svmf1_avgs)/len(svmf1_avgs)
    me_accuracy = reduce(lambda x,y: x+y,meaccuracy_avgs)/len(meaccuracy_avgs)
    me_precision = reduce(lambda x,y: x+y,meprecision_avgs)/len(meprecision_avgs)
    me_recall = reduce(lambda x,y: x+y,merecall_avgs)/len(merecall_avgs)
    me_f1_score = reduce(lambda x,y: x+y,mef1_avgs)/len(mef1_avgs)
    
    data = {'Naive Bayes': [nb_accuracy, nb_precision, nb_recall, nb_f1_score],
            'SVM': [svm_accuracy, svm_precision, svm_recall, svm_f1_score],
            'Maximum Entropy': [me_accuracy, me_precision, me_recall, me_f1_score]}
    plotting.plot_performance_histogram(data, "polarity_"+feature_set)
    return data

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
    
def train_and_test_dataset_increase():
    datasetnr = 3
    tweets = utils.get_pickles(datasetnr)
    sentimentvalues = feat_utils.get_sentiment_values(datasetnr)
    tweets = preprocessing.remove_link_classes(tweets)
    tweets = preprocessing.lower_case(tweets)
    tweets = preprocessing.remove_specialchars_round2(tweets)
    accuracy_data = {'NB(SA)':[],'NB(SB)':[],'NB(SC)':[],
            'SVM(SA)':[],'SVM(SB)':[],'SVM(SC)':[],
            'MaxEnt(SA)':[],'MaxEnt(SB)':[],'MaxEnt(SC)':[],
            'NB(PA)':[],'NB(PB)':[],'NB(PC)':[],
            'SVM(PA)':[],'SVM(PB)':[],'SVM(PC)':[],
            'MaxEnt(PA)':[],'MaxEnt(PB)':[],'MaxEnt(PC)':[]}
    f1_data = {'NB(SA)':[],'NB(SB)':[],'NB(SC)':[],
            'SVM(SA)':[],'SVM(SB)':[],'SVM(SC)':[],
            'MaxEnt(SA)':[],'MaxEnt(SB)':[],'MaxEnt(SC)':[],
            'NB(PA)':[],'NB(PB)':[],'NB(PC)':[],
            'SVM(PA)':[],'SVM(PB)':[],'SVM(PC)':[],
            'MaxEnt(PA)':[],'MaxEnt(PB)':[],'MaxEnt(PC)':[]}
    for i in range(5,101,5):
        print "=============================DATAPOINT NR. ",i,"========================================"
        data = train_subjectivity_and_test_on_feature_set(tweets, 'SA', sentimentvalues, reduce_dataset=i*0.01)
        print "DATA -- ",data
        accuracy_data['NB(SA)'].append(data['Naive Bayes'][0])
        f1_data['NB(SA)'].append(data['Naive Bayes'][3])
        accuracy_data['SVM(SA)'].append(data['SVM'][0])
        f1_data['SVM(SA)'].append(data['SVM'][3])
        accuracy_data['MaxEnt(SA)'].append(data['Maximum Entropy'][0])
        f1_data['MaxEnt(SA)'].append(data['Maximum Entropy'][3])
        
        data = train_subjectivity_and_test_on_feature_set(tweets, 'SB', sentimentvalues, reduce_dataset=i*0.01)
        print "DATA -- ",data
        accuracy_data['NB(SB)'].append(data['Naive Bayes'][0])
        f1_data['NB(SB)'].append(data['Naive Bayes'][3])
        accuracy_data['SVM(SB)'].append(data['SVM'][0])
        f1_data['SVM(SB)'].append(data['SVM'][3])
        accuracy_data['MaxEnt(SB)'].append(data['Maximum Entropy'][0])
        f1_data['MaxEnt(SB)'].append(data['Maximum Entropy'][3])
        
        data = train_subjectivity_and_test_on_feature_set(tweets, 'SC', sentimentvalues, reduce_dataset=i*0.01)
        print "DATA -- ",data
        accuracy_data['NB(SC)'].append(data['Naive Bayes'][0])
        f1_data['NB(SC)'].append(data['Naive Bayes'][3])
        accuracy_data['SVM(SC)'].append(data['SVM'][0])
        f1_data['SVM(SC)'].append(data['SVM'][3])
        accuracy_data['MaxEnt(SC)'].append(data['Maximum Entropy'][0])
        f1_data['MaxEnt(SC)'].append(data['Maximum Entropy'][3])
    
        data = train_polarity_and_test_on_feature_set(tweets, 'PA', sentimentvalues, reduce_dataset=i*0.01)
        print "DATA -- ",data
        accuracy_data['NB(PA)'].append(data['Naive Bayes'][0])
        f1_data['NB(PA)'].append(data['Naive Bayes'][3])
        accuracy_data['SVM(PA)'].append(data['SVM'][0])
        f1_data['SVM(PA)'].append(data['SVM'][3])
        accuracy_data['MaxEnt(PA)'].append(data['Maximum Entropy'][0])
        f1_data['MaxEnt(PA)'].append(data['Maximum Entropy'][3])
        
        data = train_polarity_and_test_on_feature_set(tweets, 'PB', sentimentvalues, reduce_dataset=i*0.01)
        print "DATA -- ",data
        accuracy_data['NB(PB)'].append(data['Naive Bayes'][0])
        f1_data['NB(PB)'].append(data['Naive Bayes'][3])
        accuracy_data['SVM(PB)'].append(data['SVM'][0])
        f1_data['SVM(PB)'].append(data['SVM'][3])
        accuracy_data['MaxEnt(PB)'].append(data['Maximum Entropy'][0])
        f1_data['MaxEnt(PB)'].append(data['Maximum Entropy'][3])
        
        data = train_polarity_and_test_on_feature_set(tweets, 'PC', sentimentvalues, reduce_dataset=i*0.01)
        print "DATA -- ",data
        accuracy_data['NB(PC)'].append(data['Naive Bayes'][0])
        f1_data['NB(PC)'].append(data['Naive Bayes'][3])
        accuracy_data['SVM(PC)'].append(data['SVM'][0])
        f1_data['SVM(PC)'].append(data['SVM'][3])
        accuracy_data['MaxEnt(PC)'].append(data['Maximum Entropy'][0])
        f1_data['MaxEnt(PC)'].append(data['Maximum Entropy'][3])
        out = open('incremental_acc'+str(i), 'wb')
        pickle.dump(accuracy_data, out)
        out = open('incremental_f1'+str(i), 'wb')
        pickle.dump(f1_data, out)
    plotting.plot_temporal_sentiment(accuracy_data, filename="incremental_accuracy")
    plotting.plot_temporal_sentiment(f1_data, filename="incremental_f1")
    
def test_aggregated_sentiments():
    sub_clf = classifier.get_optimal_subjectivity_classifier()
    pol_clf = classifier.get_optimal_polarity_classifier()
    tweets = utils.get_pickles(2)
    sentimentvalues = utils.get_sentimentvalues(2)
    sub_train_tweets, sub_train_targets, _, _, sub_train_sentiments, _ = utils.make_subjectivity_train_and_test_and_targets(tweets, sentimentvalues, splitvalue=1.0)
    pol_train_tweets, pol_train_targets, _, _, pol_train_sentiments, _ = utils.make_polarity_train_and_test_and_targets(tweets, sentimentvalues, splitvalue=1.0)
    
    sub_predictions = sub_clf.classify(sub_train_tweets, sub_train_sentiments)
    pol_predictions = pol_clf.classify(pol_train_tweets, pol_train_sentiments)
    print pol_train_targets, pol_predictions
    days, targets, predicts, total_frequencies = utils.temporally_aggregate_subjectivity(sub_train_tweets, sub_predictions, targets=sub_train_targets)
    data = {'Targets': [days, targets], 'Predictions': [days, predicts], 'Frequencies': [days,total_frequencies]}
    plotting.plot_subjectivity_aggregates(data, 'aggregated_subjectivity')
    days, targets, predicts, frequencies = utils.temporally_aggregate_polarity(pol_train_tweets, pol_predictions, targets=pol_train_targets)
    for i in range(len(days)):
        targets[i]=targets[i]*1.0/frequencies[i]
        predicts[i]=predicts[i]*1.0/frequencies[i]
        frequencies[i]=frequencies[i]*1.0/total_frequencies[i]
    data = {'Targets': [days, targets], 'Predictions': [days, predicts], 'Frequencies': [days,frequencies]}
    plotting.plot_polarity_aggregates(data, 'aggregated_polarity')
    
def test_remporal_topics():
    tweets1 = pickle.load(open('temporal_tweets1', 'rb'))
    tweets2 = pickle.load(open('temporal_tweets2', 'rb'))
    tweets = tweets1 + tweets2
    print len(tweets)
    sentiments = pickle.load(open('temporal_sentiments','rb'))
    print len(sentiments)
    subclf = classifier.get_optimal_subjectivity_classifier()
    polclf = classifier.get_optimal_polarity_classifier() 
    #TODO SKRIVE HER TEMPORALLY AGGREGATE ETC
    sub_predictions = subclf.classify(tweets, sentiments)
    subjective_tweets = [t for p,t in zip(sub_predictions,tweets) if p=="subjective"]
    subjective_sentiments = [s for p,s in zip(sub_predictions,sentiments) if p=="subjective"]
    pol_predictions = polclf.classify(subjective_tweets, subjective_sentiments)
    topics = entity_extraction.perform_entity_extraction(subjective_tweets, subjective_sentiments, use_pmi=True, breakword_min_freq=0.1, breakword_range=14)
    days, unique_topics, aggregated_values = utils.topically_aggregate_polarity(subjective_tweets, pol_predictions, topics=topics)
    data = {}
    for i in range(len(unique_topics)):
        data[unique_topics[i]] = [days, aggregated_values[i]]
    print data
    pickle.dump(data, open('topically_aggregated_polarity', 'wb'))

def preprocess_temporal_dataset():
    tweetlines = utils.get_dataset(utils.complete_datasets[3])
    tweets = []
    for line in tweetlines:
        if len(line)>1:
            tweets.append(tweet.to_tweet(line))
    tweets = preprocessing.preprocess_tweets(tweets)
    sentiments = lexicon.perform_google_sentiment_lexicon_lookup(tweets)
    pickle.dump(sentiments, open('temporal_sentiments','wb'))
    pickle.dump(tweets, open('temporal_tweets2', 'wb'))
    
if __name__ == '__main__':
    datasetnr = 3
    tweets = utils.get_pickles(datasetnr)
    sentimentvalues = feat_utils.get_sentiment_values(datasetnr)
    tweets = preprocessing.remove_link_classes(tweets)
    tweets = preprocessing.lower_case(tweets)
    tweets = preprocessing.remove_specialchars_round2(tweets)
    
    train_subjectivity_and_test_on_feature_set(tweets, 'SA', datasetnr)
    train_subjectivity_and_test_on_feature_set(tweets, 'SB', datasetnr)
    train_subjectivity_and_test_on_feature_set(tweets, 'SC', sentimentvalues)
    
    train_polarity_and_test_on_feature_set(tweets, 'PA', datasetnr)
    train_polarity_and_test_on_feature_set(tweets, 'PB', datasetnr)
    train_polarity_and_test_on_feature_set(tweets, 'PC', sentimentvalues)