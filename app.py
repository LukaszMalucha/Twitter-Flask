##### App Utilities
import os
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, current_app, request, redirect, url_for, flash


##### Twitter API
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



################################################################### APP SETTINGS ###########################

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY") 
Bootstrap(app)

### Twitter Authentication

CONSUMER_KEY = os.environ.get("CONSUMER_KEY") 
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET") 
OAUTH_TOKEN = os.environ.get("OAUTH_TOKEN") 
OAUTH_TOKEN_SECRET = os.environ.get("OAUTH_TOKEN_SECRET") 

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

api = tweepy.API(auth)



################################################################### VIEWS ################################

## Home
@app.route('/')
@app.route('/interface')
def interface():
    
    return render_template("interface.html")
    
    
###### Trends Intersection    
@app.route('/twitter_trends')
def twitter_trends():
    
    
    return render_template("twitter_trends.html")
    
    
@app.route('/common_trends', methods=['POST'])
def common_trends():
    
    city_1 = request.form.get('city_1')
    city_2 = request.form.get('city_2')
    
    city_1_trends = api.trends_place(city_1)
    city_2_trends = api.trends_place(city_2)
    
    city_1_trends_set = set([trend['name'] for trend in city_1_trends[0]['trends']])
    city_2_trends_set = set([trend['name'] for trend in city_2_trends[0]['trends']])
    
    common_trends = set.intersection(city_1_trends_set, city_2_trends_set)
    
    
    return render_template("common_trends.html", common_trends = common_trends)    


##### 










################################################################## APP INITIATION ########################


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 