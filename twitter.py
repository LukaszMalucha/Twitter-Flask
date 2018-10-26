import os
import env
import json
import tweepy
from tweepy import OAuthHandler

CONSUMER_KEY = os.environ.get("CONSUMER_KEY") 
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET") 
OAUTH_TOKEN = os.environ.get("OAUTH_TOKEN") 
OAUTH_TOKEN_SECRET = os.environ.get("OAUTH_TOKEN_SECRET") 