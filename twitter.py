import os
import env
import json
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from collections import Counter
from prettytable import PrettyTable
from operator import itemgetter


### REQUIRES PYTON 3.6, async won't work on 3.7

CONSUMER_KEY = os.environ.get("CONSUMER_KEY") 
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET") 
OAUTH_TOKEN = os.environ.get("OAUTH_TOKEN") 
OAUTH_TOKEN_SECRET = os.environ.get("OAUTH_TOKEN_SECRET") 


auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


api = tweepy.API(auth)

# DUB_WOE_ID = 560743
# LON_WOE_ID = 44418


# # Common Hashatgs
# dub_trends = api.trends_place(DUB_WOE_ID)
# lon_trends = api.trends_place(LON_WOE_ID)

# dub_trends_set = set([trend['name'] for trend in dub_trends[0]['trends']])
# lon_trends_set = set([trend['name'] for trend in lon_trends[0]['trends']])

# common_trends = set.intersection(dub_trends_set, lon_trends_set)

# print(dub_trends_set, common_trends)

# ## Get Tweets

# count = 10
# query = 'Dublin'

# results = [status for status in tweepy.Cursor(api.search, q=query).items(count)]


# for result in results:
#     print(json.dumps(result._json, indent=4))

# for status in results:
#     print(status.text.encode('utf-8'))
#     print(status.user.id)
#     print(status.user.screen_name)
#     print(status.user.profile_image_url_https)
#     print(status.user.followers_count)
#     print(status.place)




## Get all tweets for the search query

# count = 50
# query = 'Dublin'

# results = [status for status in tweepy.Cursor(api.search, q=query).items(count)]

# status_texts = [status._json['text'] for status in results]

# screen_names = [status._json['user']['screen_name'] 
#                     for status in results
#                         for mention in status._json['entities']['user_mentions']]


# hashtags = [hashtag['text']
#                         for status in results
#                             for hashtag in status._json['entities']['hashtags']]
                        

# words = [ word 
#                 for text in status_texts
#                     for word in text.split() ]   
                    
# print(json.dumps(status_texts[0:5], indent=1))           
# print(json.dumps(screen_names[0:5], indent=1))
# print(json.dumps(hashtags[0:5], indent=1))
# print(json.dumps(words[0:5], indent=1))



# ## Get all tweets for the search query

# count = 50
# query = 'Khashoggi'

# results = [status for status in tweepy.Cursor(api.search, q=query).items(count)]

# status_texts = [status._json['text'] for status in results]

# screen_names = [status._json['user']['screen_name'] 
#                     for status in results
#                         for mention in status._json['entities']['user_mentions']]


# hashtags = [hashtag['text']
#                         for status in results
#                             for hashtag in status._json['entities']['hashtags']]
                        

# words = [ word 
#                 for text in status_texts
#                     for word in text.split() ]   
                    
# for entry in [screen_names, hashtags, words]:
#     counter = Counter(entry)
#     print(counter.most_common()[:10])
    
    
    
## Lexical Diversity

# count = 50
# query = 'Khashoggi'

# results = [status for status in tweepy.Cursor(api.search, q=query).items(count)]

# status_texts = [status._json['text'] for status in results]

# screen_names = [status._json['user']['screen_name'] 
#                     for status in results
#                         for mention in status._json['entities']['user_mentions']]


# hashtags = [hashtag['text']
#                         for status in results
#                             for hashtag in status._json['entities']['hashtags']]
                        

# words = [ word 
#                 for text in status_texts
#                     for word in text.split() ]   
                    
# for entry in [screen_names, hashtags, words]:
#     counter = Counter(entry)
#     print(counter.most_common()[:10])    
    
# def get_lexical_diversity(items):
#     return 1.0*len(set(items))/len(items)
    
# def get_average_words(tweets):
#     total_words = sum([len(tweet.split()) for tweet in tweets])
#     return 1.0*total_words/len(tweets)
    
# print("Average words: {0}".format(get_average_words(status_texts)))    
# print("Word Diversity: {0}".format(get_lexical_diversity(words)))
# print("Screen Name Diversity: {0}".format(get_lexical_diversity(screen_names)))
# print("Hashtag Diversity: {0}".format(get_lexical_diversity(hashtags)))


### RETWEET POPULARITY

# count = 150
# query = 'Khashoggi'

# ## get tweets for the search query

# results = [status for status in tweepy.Cursor(api.search, q=query).items(count)]

# min_retweets = 10 ## retweet treshold

# pop_tweets = [status
#                 for status in results
#                     if status._json['retweet_count'] > min_retweets]

# ## tuple of tweet + retweet count                    
# tweet_tups = [(tweet._json['text'].encode('utf-8'), tweet._json['retweet_count'])
#                 for tweet in pop_tweets]
                
# ## sort descending
# most_popular_tups = sorted(tweet_tups, key=itemgetter(1), reverse=True)[:5]


# # prettify
# table = PrettyTable(field_names=['Text', 'Retweet Count'])
# for key, val in most_popular_tups:
#     table.add_row([key, val])
# table.max_width['Text'] = 50
# table.align['Text'], table.align['Retweet Count'] = 'l', 'r'  # align the columns
# print(table)

# ### TWITTER USER INFO


# user = api.get_user('@realDonaldTrump')

# print(user.screen_name)
# print(user.followers_count)

# for friend in user.friends():
#     print(friend.screen_name)
#     print(friend.followers_count)


# ## TWEETS FROM THE USER TIMELINE


# for status in tweepy.Cursor(api.home_timeline).items(10):
    
#     print(status.text)


### ACCESS TWITTER STREAM 

keyword_list = ['python', 'javascript', 'php', 'C#']

limit = 10

class MyStreamListener(StreamListener):
    
    def __init__(self):
        super(MyStreamListener, self).__init__()
        self.num_tweets = 0
        
    def on_data(self, data):
        if self.num_tweets < limit: 
            self.num_tweets += 1
            try:
                with open('tweet_mining.json', 'a') as tweet_file:
                    tweet_file.write(data)
                    return True
            except BaseException as e:
                print("Failed %s"%str(e))
            return True 
        else:
            return False
        
    def on_error(self, status):
        print(status)
        return True
        
        
twitter_stream = Stream(auth, MyStreamListener())
twitter_stream.filter(track=keyword_list)