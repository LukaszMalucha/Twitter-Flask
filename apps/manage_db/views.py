from flask import Blueprint


## BLUEPRINT INIT

manage_db_blueprint = Blueprint(
    'manage_db_blueprint', __name__,
    template_folder="templates"
    )
    
from app import *    



###################################################### Database Management   
    
    
@manage_db_blueprint.route('/manage_db', methods=['GET', 'POST'])
def manage_db(): 
    
    mongo_hashtags = mongo.db.harvest_tweets.distinct("hashtag")
    
    
    sqlite_hashtags = list(db.session.query(Tweets.hashtag.distinct()))
    
    return render_template("manage_db.html", mongo_hashtags = mongo_hashtags, 
                                            sqlite_hashtags = sqlite_hashtags)
                                       
                                       
                                       
@manage_db_blueprint.route('/delete_mongodb_tweets/<hashtag>', methods=['GET', 'POST'])
def delete_mongodb_tweets(hashtag):   
    
    mongo.db.harvest_tweets.remove({"hashtag": hashtag})
    
    
    return redirect(url_for('manage_db_blueprint.manage_db'))


@manage_db_blueprint.route('/delete_sql_tweets/<hashtag>', methods=['GET', 'POST'])
def delete_sql_tweets(hashtag):   
    
    Tweets.query.filter_by(hashtag=hashtag).delete()
    db.session.commit()
    
    
    return redirect(url_for('manage_db_blueprint.manage_db'))
  
  