'''
Created on 10. mars 2014

@author: JohnArne
'''
#Retrieves tweets from website using curl calls, and stores it locally.

import urllib
import urllib2
import json
#import pycurl
import requests


#def retrieve_tweets_curl():
#    url_string = 'http://vm-6123.idi.ntnu.no:9200/_all/_search?pretty'
#    query_string = '{"from":0, "size":100, "query": {"match_all": {}}, "filter": {"bool": {"must": [ {"match_all": {}}, {"terms": {"_type": ["\"article\""] }}, {"fquery": {"query": {"field": {"type": {"query": "\"tweet\""}}}}}] }}, "sort": [ {"published": {"order": "\"desc\"" }} ] }' 
#    query = '{"match_all": {}}'
#    filter = '{"bool": {"must": [ {"match_all": {}}, {"terms": {"_type": ["\"article\""] }}, {"fquery": {"query": {"field": {"type": {"query": "\"tweet\""}}}}}] }}'
#    sort = '[ {"published": {"order": "\"desc\"" }} ]'
#    print pycurl.version_info()
#    
#    return tweets

"""
Retrieve tweets using web request.
"""
def retrieve_tweets():
    url_string = 'http://vm-6123.idi.ntnu.no:9200/_all/_search?pretty'
    query_string = '{"from":0, "size":100, "query": {"match_all": {}}, "filter": {"bool": {"must": [ {"match_all": {}}, {"terms": {"_type": ["\"article\""] }}, {"fquery": {"query": {"field": {"type": {"query": "\"tweet\""}}}}}] }}, "sort": [ {"published": {"order": "\"desc\"" }} ] }' 
    query = '{"match_all": {}}'
    filter = '{"bool": {"must": [ {"match_all": {}}, {"terms": {"_type": ["\"article\""] }}, {"fquery": {"query": {"field": {"type": {"query": "\"tweet\""}}}}}] }}'
    sort = '[ {"published": {"order": "\"desc\"" }} ]'
    
    params = {'from': 0,
              'size': 10
              }
#              'query': {"match_all": {}},
#              'filter': {"bool": {"must": [ {"match_all": {}}, {"terms": {"_type": ["article"] }}, {"fquery": {"query": {"field": {"type": {"query": "tweet"}}}}}] }},
#              'sort': [ {"published": {"order": "\"desc\"" }} ]
#              }
    
    data = urllib.urlencode(params)
    request = urllib2.Request(url_string, data)
    
    print "Request" + str(request.get_data())
    
    response = urllib2.urlopen(request)
    tweets = response.read()
    
    return tweets

def retrieve_tweets_by_requests():
    url_string = 'http://vm-6123.idi.ntnu.no:9200/_all/_search?pretty'
    query_string = '{"from":0, "size":100, "query": {"match_all": {}}, "filter": {"bool": {"must": [ {"match_all": {}}, {"terms": {"_type": ["\"article\""] }}, {"fquery": {"query": {"field": {"type": {"query": "\"tweet\""}}}}}] }}, "sort": [ {"published": {"order": "\"desc\"" }} ] }' 
    
    
    return tweets


#Store the tweets in a tsv with only necessary information    
def store_tweets():
    file = None
    
if __name__ == '__main__':
    tweets = retrieve_tweets()
    print "twat" + tweets
    