from flask import Blueprint, render_template


## BLUEPRINT INIT

api_features_blueprint = Blueprint(
    'api_features_blueprint', __name__,
    template_folder="templates"
    )


########################################## City Trends Intersection

## http://www.woeidlookup.com/

@api_features_blueprint.route('/twitter_trends')
def twitter_trends():
    message = ""
    return render_template("twitter_trends.html", message=message)
