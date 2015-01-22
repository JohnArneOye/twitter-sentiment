
import tweepy
import utils

OAUTH_API_KEY = "JvgeRvICbMtWYcmhTug3w"
OAUTH_API_SECRET = "CzIwJm5yUi6hTHeLjrYMHZIMoszkNCD1MqgHFfO5qI"

ACCESS_TOKEN = "462254796-mLqIDTfa1e0ODYfksV1CiEunCIT5MuJ3avvp2kt9"
ACCESS_SECRET = "EsRjaoF8ZAkQSNEk8s72Kf3aEStFV3k4epBLMsefDZtKd"

class TweetRetriever(object):
    """
    Handler for retrieving tweets using the twitter API through Tweepy.
    """
    
    query = ""
    def __init__(self, query):
        auth = tweepy.OAuthHandler(OAUTH_API_KEY, OAUTH_API_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        self.api = tweepy.API(auth)
        print "Connection to Twitter API is up."
        
        arguments = query.split(' ')
        if len(arguments)>2:
            self.since=arguments[len(arguments)-2]
            self.until=arguments[len(arguments)-1]
            self.query = " ".join(arguments[:len(arguments)-2])
        else:
            self.since=None
            self.until=None
            self.query = query

    def retrieve_for_dataset(self):
        """
        Return a sample of tweets and add to current dataset text file
        """
        if self.since == None and self.until==None:
            c = tweepy.Cursor(self.api.search, q=self.query, lang="no")
        else:
            c = tweepy.Cursor(self.api.search, q=self.query, since=self.since,until=self.until,lang="no")
        results = []
        print self.query
        print self.since
        print self.until
        for tweet in c.items(500):
            results.append(tweet)
        results_list = utils.get_resultsets_text(results)
        dataset = utils.select_complete_dataset()
        utils.append_to_dataset(results_list, dataset)
        print "Fetched "+str(len(results_list)) +" tweets"
    
    def retrieve_as_tweets(self):
        """
        Fetch a sample of tweets and return them as tweets objects
        """
        tweets = []
        return tweets
        
    def retrieve_stream(self):
        """
        Fetch tweets from the twitter stream.
        """
        tweets =[]
        return tweets