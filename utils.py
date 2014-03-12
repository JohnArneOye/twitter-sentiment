'''
Created on 12. mars 2014

@author: JohnArne
'''

def load_to_tsv():
    json_data = open("data/curl_twitterdata.json")
    data = json.load(json_data)
#    pprint(data)
    tweets = [ x["_source"]["published"]+str("\t")+x["_source"]["publisher"]+str("\t")+x["_source"]["leadText"] for x in data["hits"]["hits"] ]
    for tweet in tweets:
        print tweet
    print len(tweets)
    out = csv.writer(open("data/dataset.tsv","w"), delimiter="\n", quoting=csv.QUOTE_MINIMAL)
    out.writerow(tweets)
    json_data.close()