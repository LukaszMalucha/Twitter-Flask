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

# Get all tweets for the search query hashtag

count = 5
query = '#Dublin'
if query[0] != '#':
    query = '#'+'Dublin'

# print(query)

results = [status for status in tweepy.Cursor(api.search, q=query).items(count)]


for tweet in tweepy.Cursor(api.search, q=query).items(count):
    data = {}
    data['created_at'] = tweet.created_at
    data['retweet_count'] = tweet.retweet_count
    data['id'] = tweet.id
    data['text'] = tweet.text
    data['location'] = tweet.user.location
    print(data)





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
                    
# tweet_list = [[tweet._json['text'], tweet._json['created_at'][:19], tweet._json['user']['name'], tweet._json['retweet_count']]
#                     for tweet in results]                    

# for element in status_texts:                    
#     print(element)
#     print('')
                    
                    
