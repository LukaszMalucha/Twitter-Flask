################################################################## App Utilities
import os
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, current_app, request, redirect, url_for, flash, session


####################################################################### Mongo DB

from flask_pymongo import PyMongo
from bson.objectid import ObjectId

########################################################################## MySQL

from flask_sqlalchemy import SQLAlchemy

#################################################################### Twitter API
import os
import env
import json
import tweepy                # REQUIRES PYTON 3.6, async won't work on 3.7
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from collections import Counter
from prettytable import PrettyTable
from operator import itemgetter


################################################################## Data Analysis

import re

## get rid of irrelevant and stemming words:
import nltk   
# nltk.download('stopwords')          ## stopwords list
from nltk.corpus import stopwords 

## getting the root of every word (stemming):
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()



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



## BLUE

from features.views import features_blueprint
app.register_blueprint(features_blueprint)

api = tweepy.API(auth)

#### SQLite Classes

class Tweets(db.Model):
    __tablename__ = 'tweets'
    id = db.Column('id', db.Integer, primary_key=True)
    hashtag = db.Column('hashtag', db.Unicode)
    tweet = db.Column('tweet', db.Unicode)
    
    # def __init__(self, id, hashtag, tweet):
    #     self.id = id
    #     self.hashtag = hashtag
    #     self.tweet = tweet





################################################################### VIEWS ######################################################################



############################################################## Home

@app.route('/')
@app.route('/dashboard')
def dashboard():
    
    return render_template("dashboard.html")
    
    
    
##################################################### Trend Search

@app.route('/trend_search')
def trend_search():
    
    us_trends = api.trends_place(23424977)
    us_trends_list = [trend['name'] for trend in us_trends[0]['trends'][:40]]
    
    return render_template("trend_search.html", us_trends_list = us_trends_list)



@app.route('/tweets', methods=['POST'])
def tweets():
    
    harvest_tweets=mongo.db.harvest_tweets
    keyword = request.form.get('trend')
    if keyword[0] != '#':
        keyword = '#' + keyword 
    count = int(request.form.get('count'))  
    
 
    for tweet in tweepy.Cursor(api.search, q=keyword).items(count):
        data = {}
        data['text'] = tweet.text
        data['hashtag'] = keyword
        data['created_at'] = tweet.created_at
        data['retweet_count'] = tweet.retweet_count
        try:
            harvest_tweets.insert(data)
        except:
            pass

    
    results = [status for status in tweepy.Cursor(api.search, q=keyword).items(count)]
    
    tweet_list = [[tweet._json['text'], tweet._json['created_at'][:19], tweet._json['user']['name'], tweet._json['retweet_count']]
                    for tweet in results]

    return render_template("tweets.html", tweet_list = tweet_list, keyword = keyword)    
    
    
@app.route('/data_transform/<hashtag>', methods=['GET', 'POST'])
def data_transform(hashtag):  
    
    hashtag_tweets = mongo.db.harvest_tweets.find({"hashtag": hashtag})
    
    
    text = [element['text'] for element in hashtag_tweets]
    
    corpus = []
    for i in range(0,len(text)):
            tweet = re.sub('[^a-zA-Z]',' ',text[i])    ## all the indexes
            tweet = tweet.lower()
            tweet = tweet.split() 
            ps = PorterStemmer()
            tweet = [ps.stem(word) for word in tweet if not word in set(stopwords.words('english'))]
            tweet = ' '.join(tweet)
            corpus.append(tweet)
            tweet_load = Tweets(hashtag = hashtag, tweet = tweet)
            db.session.add(tweet_load)
            db.session.commit()


    return render_template("data_transform.html", text = text, corpus = corpus, hashtag = hashtag)
    
@app.route('/data_load/<hashtag>', methods=['GET', 'POST'])
def data_load(hashtag): 
    
    hashtag_tweets =  Tweets.query.filter_by(hashtag = hashtag)
    

    return render_template("data_load.html", hashtag_tweets = hashtag_tweets)
    
    
    
###################################################### Database Management   
    
    
@app.route('/manage_db', methods=['GET', 'POST'])
def manage_db(): 
    
    mongo_hashtags = mongo.db.harvest_tweets.distinct("hashtag")
    
    
    sqlite_hashtags = list(db.session.query(Tweets.hashtag.distinct()))
    
    return render_template("manage_db.html", tweets = tweets, 
                                       mongo_hashtags = mongo_hashtags, 
                                       sqlite_hashtags = sqlite_hashtags)
                                       
                                       
                                       
@app.route('/delete_mongodb_tweets/<hashtag>', methods=['GET', 'POST'])
def delete_mongodb_tweets(hashtag):   
    
    mongo.db.harvest_tweets.remove({"hashtag": hashtag})
    
    
    return redirect(url_for('manage_db'))


@app.route('/delete_sql_tweets/<hashtag>', methods=['GET', 'POST'])
def delete_sql_tweets(hashtag):   
    
    Tweets.query.filter_by(hashtag=hashtag).delete()
    db.session.commit()
    
    
    return redirect(url_for('manage_db'))
  
  

################################################################# APP INITIATION #############################################################


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 