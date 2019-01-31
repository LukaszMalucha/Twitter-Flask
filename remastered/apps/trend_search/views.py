from flask import Blueprint


## BLUEPRINT INIT

trend_search_blueprint = Blueprint(
    'trend_search_blueprint', __name__,
    template_folder="templates"
    )
    
from app import *    


################################################################### Trend Search

@trend_search_blueprint.route('/trend_search')
def trend_search():
    
    ## Get US most trending
    us_trends = api.trends_place(23424977)
    us_trends_list = [trend['name'] for trend in us_trends[0]['trends'][:40]]
    
    return render_template("trend_search.html", us_trends_list = us_trends_list)



@trend_search_blueprint.route('/tweets', methods=['POST'])
def tweets():
    
    ## Upload tweets to MongoDB
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
    
    ## Display tweets
    tweet_list = [[tweet._json['text'], tweet._json['created_at'][:19], tweet._json['user']['name'], tweet._json['retweet_count']]
                    for tweet in results]

    return render_template("tweets.html", tweet_list = tweet_list, keyword = keyword)    
    
    
    
    
@trend_search_blueprint.route('/data_transform/<hashtag>', methods=['GET', 'POST'])
def data_transform(hashtag):  
    
    ## Get chosen hashtag tweets
    hashtag_tweets = mongo.db.harvest_tweets.find({"hashtag": hashtag})
    
    ## Preprocess text for future senitment analysis
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
    
    
    
@trend_search_blueprint.route('/data_load/<hashtag>', methods=['GET', 'POST'])
def data_load(hashtag): 
    
    ## Display SQL DB tweets
    hashtag_tweets =  Tweets.query.filter_by(hashtag = hashtag)
    

    return render_template("data_load.html", hashtag_tweets = hashtag_tweets)
    
    
    
# stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", 
#     "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
#     'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 
#     'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 
#     'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 
#     'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 
#     'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there',
#     'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 
#     'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 
#     'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 
#     'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 
#     'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
    