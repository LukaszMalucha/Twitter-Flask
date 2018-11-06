from flask import Blueprint


## BLUEPRINT INIT

sentiment_blueprint = Blueprint(
    'sentiment_blueprint', __name__,
    template_folder="templates"
    )
    
from app import *    
    
    
@sentiment_blueprint.route('/sentiment_analysis')    
def sentiment_analysis():
    
    sqlite_hashtags = list(db.session.query(Tweets.hashtag.distinct()))
    
    return render_template("sentiment_analysis.html", sqlite_hashtags = sqlite_hashtags)
    
@sentiment_blueprint.route('/results')    
def results():
    
    return render_template("results.html")