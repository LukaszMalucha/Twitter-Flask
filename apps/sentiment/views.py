from flask import Blueprint


## BLUEPRINT INIT

sentiment_blueprint = Blueprint(
    'sentiment_blueprint', __name__,
    template_folder="templates"
    )
    
from app import *    

from model import load 
import pickle

global model, graph
model, graph = load.init()



    
@sentiment_blueprint.route('/sentiment_analysis')    
def sentiment_analysis():
    
    sqlite_hashtags = list(db.session.query(Tweets.hashtag.distinct()))
    
    return render_template("sentiment_analysis.html", sqlite_hashtags = sqlite_hashtags)
    
    
    
@sentiment_blueprint.route('/results/<hashtag>')    
def results(hashtag):
    
    tweets = mongo.db.harvest_tweets.find({"hashtag": hashtag})
    tweets = [element['text'] for element in tweets]
    hashtag_tweets =  Tweets.query.filter_by(hashtag = hashtag).all()
    hashtag_tweets = [ element.tweet for element in hashtag_tweets]
    
    with open('model/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
     
    results = []    
    for element in hashtag_tweets:
        element = re.sub('[^a-zA-Z]',' ',element)
        element = element.lower()   
        element = element.split()
        element = [ps.stem(word) for word in element if not word in set(stopwords.words('english'))]
        element = tokenizer.texts_to_sequences(element)    
        element = pad_sequences(element, maxlen=23, dtype='int32', value=0)
        results.append(element)

    predictions = []
    with graph.as_default():
        for element in results:
            prediction = model.predict(element,batch_size=1,verbose = 2)[0]
            if (np.argmax(prediction) == 0):
                prediction = 'Negative'
            elif (np.argmax(prediction) == 1):    
                prediction = 'Neutral'
            else:
                prediction = 'Positive'
            predictions.append(prediction)
    
    zipper = zip(tweets , predictions)        

    
    return render_template("results.html", hashtag_tweets = hashtag_tweets, predictions = predictions, zipper = zipper)
    
