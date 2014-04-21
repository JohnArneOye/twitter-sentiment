'''
Created on 10. mars 2014

@author: JohnArne
'''
import tweepy
import utils

OAUTH_API_KEY = "JvgeRvICbMtWYcmhTug3w"
OAUTH_API_SECRET = "CzIwJm5yUi6hTHeLjrYMHZIMoszkNCD1MqgHFfO5qI"

ACCESS_TOKEN = "462254796-mLqIDTfa1e0ODYfksV1CiEunCIT5MuJ3avvp2kt9"
ACCESS_SECRET = "EsRjaoF8ZAkQSNEk8s72Kf3aEStFV3k4epBLMsefDZtKd"

class TweetRetriever(object):
    
    def __init__(self):
        auth = tweepy.OAuthHandler(OAUTH_API_KEY, OAUTH_API_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        self.api = tweepy.API(auth)
        print "Connection to Twitter API is up."

#        auth = tweepy.OAuthHandler(OAUTH_API_KEY, OAUTH_API_SECRET)
#        try:
#            redirect_url = auth.get_authorization_url()
#        except tweepy.TweepError:
#            print "ERROR. Couldn't get REQUEST TOKEN URL!"
#        
#        auth.set_request_token(OAUTH_API_KEY, OAUTH_API_SECRET)
#        
#        auth.get_access_token()
#        
#        self.api.update_status("tweepy and oauth up!")
        
    #Return a sample of tweets and add to current dataset
    def retrieve_for_dataset(self, query):
        results = self.api.search(q=query, lang="no", count= 100)
        results_list = utils.get_resultsets_text(results)
        utils.append_to_dataset(results_list)
        print "Fetched "+str(len(results_list)) +" tweets"
#        for twt in results:
#            print "%s" %(twt.text)
#        utils.append_twitter_results(results)
#        for twt in results:
#            results_string = results_string + unicode(twt.created_at) +"\t"+ unicode(twt.user.screen_name) +"\t"+ unicode(twt.text)

    
    
class Tweet(object):
    
    def __init__(self):
        self.text = ""
        self.publisher = ""
        self.timestamp = ""
        self.sentiment = []
        
if __name__ == '__main__':
    retriever = TweetRetriever()
    query = "erna solberg"
    tweets = retriever.retrieve_for_dataset(query)