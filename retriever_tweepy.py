
import tweepy
import utils

OAUTH_API_KEY = "JvgeRvICbMtWYcmhTug3w"
OAUTH_API_SECRET = "CzIwJm5yUi6hTHeLjrYMHZIMoszkNCD1MqgHFfO5qI"

ACCESS_TOKEN = "462254796-mLqIDTfa1e0ODYfksV1CiEunCIT5MuJ3avvp2kt9"
ACCESS_SECRET = "EsRjaoF8ZAkQSNEk8s72Kf3aEStFV3k4epBLMsefDZtKd"

class TweetRetriever(object):
    
    query = ""
    def __init__(self, query):
        auth = tweepy.OAuthHandler(OAUTH_API_KEY, OAUTH_API_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        self.api = tweepy.API(auth)
        print "Connection to Twitter API is up."
        self.query = query

     
    #Return a sample of tweets and add to current dataset text file
    def retrieve_for_dataset(self):
        results = self.api.search(q=self.query, lang="no", count= 100)
        results_list = utils.get_resultsets_text(results)
        utils.append_to_dataset(results_list)
        print "Fetched "+str(len(results_list)) +" tweets"
    
    #Fetch a sample of tweets and return them as tweets objects
    def retrieve_as_tweets(self):
        tweets = []
        return tweets
    
    
class Tweet(object):
    
    def __init__(self):
        self.user = ""
        self.text = ""
        self.timestamp = ""
        self.subjectivity = 0
        self.polarity = 0
        
if __name__ == '__main__':
    retriever = TweetRetriever("erna solberg")
    tweets = retriever.retrieve_for_dataset()