from flask import Blueprint


## BLUEPRINT INIT

features_blueprint = Blueprint(
    'features_blueprint', __name__,
    template_folder="templates"
    )
    
from app import *    
    
 
########################################## City Trends Intersection 

## http://www.woeidlookup.com/

@features_blueprint.route('/twitter_trends')
def twitter_trends():
    
    message = ""
    return render_template("twitter_trends.html", message=message)
    
    
@features_blueprint.route('/common_trends', methods=['GET','POST'])
def common_trends():
    
    city_1 = request.form.get('city_1')
    city_2 = request.form.get('city_2')
    
    try:
        city_1_trends = api.trends_place(city_1)
        city_2_trends = api.trends_place(city_2)
        
        # if city_1_trends and city_2_trends:
            
        city_1_trends_set = set([trend['name'] for trend in city_1_trends[0]['trends']])
        city_2_trends_set = set([trend['name'] for trend in city_2_trends[0]['trends']])
        
        common_trends = set.intersection(city_1_trends_set, city_2_trends_set)
        
        clean_trends = []
        for trend in common_trends:
            trend = trend.replace('#','')
            clean_trends.append(trend)
            
        clean_trends = sorted(clean_trends)
        
        return render_template("common_trends.html", clean_trends = clean_trends)    
    
    except:
    
        return render_template("twitter_trends.html", 
                              message="Requested ID does not exist, try another one:" )
        


################################################ Retweet popularity    

@features_blueprint.route('/retweet_popularity')
def retweet_popularity():
    
    return render_template("retweet_popularity.html")    
    
    
@features_blueprint.route('/most_retweets', methods=['POST'])
def most_retweets():
    
    keyword = request.form.get('keyword')
    count = int(request.form.get('count'))
    min_retweets = int(request.form.get('retweets'))
    
    ## get tweets for the search query

    results = [status for status in tweepy.Cursor(api.search, q=keyword).items(count)]
    
    
    pop_tweets = [status
                    for status in results
                        if status._json['retweet_count'] > min_retweets]
    
    ## tuple of tweet + retweet count                    
    tweet_list = [[tweet._json['text'], tweet._json['created_at'][:19], tweet._json['user']['name'], tweet._json['retweet_count']]
                    for tweet in pop_tweets]
                    
    ## sort descending
    most_popular_tweets = sorted(tweet_list, key=itemgetter(1), reverse=True)[:count]
    
    return render_template("most_retweets.html", most_popular_tweets = most_popular_tweets)
    

################################################################# APP INITIATION #############################################################
    
    
    
    