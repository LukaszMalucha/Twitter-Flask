################################################################## App Utilities
import os
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, redirect, url_for


####################################################################### Mongo DB

from flask_pymongo import PyMongo

########################################################################## MySQL

from flask_sqlalchemy import SQLAlchemy

#################################################################### Twitter API
import os
import env
import json
import tweepy                # REQUIRES PYTON 3.6, async won't work on 3.7
from tweepy import OAuthHandler


############################################################# Sentiment Analysis

import re
## get rid of irrelevant and stemming words:
import nltk   
# nltk.download('stopwords')          ## stopwords list
from nltk.corpus import stopwords 

## getting the root of every word (stemming):
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

import keras
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM
from keras.preprocessing.text import Tokenizer
from keras.models import load_model



################################################################### APP SETTINGS ##############################################################

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY") 
Bootstrap(app)

### Mongo DB

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME") 
app.config["MONGO_URI"] = os.environ.get("MONGO_URI") 
mongo = PyMongo(app)

### SQLite

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tweets.db'
db = SQLAlchemy(app)

### Twitter Authentication

CONSUMER_KEY = os.environ.get("CONSUMER_KEY") 
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET") 
OAUTH_TOKEN = os.environ.get("OAUTH_TOKEN") 
OAUTH_TOKEN_SECRET = os.environ.get("OAUTH_TOKEN_SECRET") 

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

api = tweepy.API(auth)

################################################################# SQLITE CLASSES ###################################################

## For uploading tweets to sqlite
class Tweets(db.Model):
    __tablename__ = 'tweets'
    id = db.Column('id', db.Integer, primary_key=True)
    hashtag = db.Column('hashtag', db.Unicode)
    tweet = db.Column('tweet', db.Unicode)
    
    # def __init__(self, id, hashtag, tweet):
    #     self.id = id
    #     self.hashtag = hashtag
    #     self.tweet = tweet


##################################################################### BLUEPRINTS ###################################################

from apps.features.views import features_blueprint
from apps.manage_db.views import manage_db_blueprint
from apps.trend_search.views import trend_search_blueprint
from apps.sentiment.views import sentiment_blueprint

app.register_blueprint(features_blueprint)
app.register_blueprint(manage_db_blueprint)
app.register_blueprint(trend_search_blueprint)
app.register_blueprint(sentiment_blueprint)

################################################################### VIEWS ######################################################################



############################################################## Home

@app.route('/')
@app.route('/dashboard')
def dashboard():
    
    return render_template("dashboard.html")
    
    

################################################################# APP INITIATION #############################################################


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 