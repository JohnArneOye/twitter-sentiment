
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
        self.query = query

    def retrieve_for_dataset(self):
        """
        Return a sample of tweets and add to current dataset text file
        """
        c = tweepy.Cursor(self.api.search, q=self.query, lang="no")
        results = []
        for tweet in c.items():
            results.append(tweet)
        results_list = utils.get_resultsets_text(results)
        utils.append_to_dataset(results_list)
        print "Fetched "+str(len(results_list)) +" tweets"
    
    def retrieve_as_tweets(self):
        """
        Fetch a sample of tweets and return them as tweets objects
        """
        tweets = []
        return tweets
    
class Tweet(object):
    """
    Class for wrapping tweet information.
    """
    
    def __init__(self):
        self.user = ""
        self.text = ""
        self.timestamp = ""
        self.subjectivity = 0
        self.polarity = 0
        
    def to_tsv(self):
        """
        Convert the data in this tweet to the .tsv format used to store it in .tsv files.
        """
        return ""
    
def to_tweet(self, text):
    """
    Convert a given .tsv formatted text line to a tweet object
    """
    return Tweet()
        

        
        
if __name__ == '__main__':
    retriever = TweetRetriever("erna solberg")
    tweets = retriever.retrieve_for_dataset()