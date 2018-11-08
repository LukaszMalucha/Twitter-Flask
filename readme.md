## Twitter API Dashboard

### Link to Application:
[Heroku App](https://twitter-api-dashboard.herokuapp.com/)


## PROJECT OVERVIEW

Project Goal was to create fully functional interface for Twitter API. Flask App allows user to find out what is currently trending and extract data sample to MongoDB.
Once data sample is extracted, next step is to preprocess it and load to SQL database. Final step is to apply Keras LSTM model on processed tweets to find out what's the dominating sentiment 
among conversation participants - positive, negatve or neutral.



## APP STRUCTURE


### Main Dashboard View

Choose between app main functionalities:
<br>

![1](https://user-images.githubusercontent.com/26208598/48212361-5749d200-e373-11e8-9e1c-de0939c4b5b0.PNG)

<br>

### Trend Search

Find out what is currently trending in US. Pick most interesting subject and guide your data sample through ETL pipeline to make it ready for sentiment analysis.
<br>

![2](https://user-images.githubusercontent.com/26208598/48212444-83655300-e373-11e8-948e-c984afd52462.PNG)

<br>

### Manage Database

Get rid of obsolete collections from MongoDB or delete processed data from SQLite database:  
<br>

![4](https://user-images.githubusercontent.com/26208598/48212709-10101100-e374-11e8-9ed7-12197bf6fa38.PNG)

<br>

### Sentiment Analysis 

Apply Deep learning LSTM model on previously stored Twitter dataset. Find out what's the dominating sentiment among conversation participants - positive, negatve or neutral.
<br>

![3](https://user-images.githubusercontent.com/26208598/48212751-303fd000-e374-11e8-9b68-b49d9677d8ad.PNG)

<br>

### Tale of Two Cities

Find out what is currently trending in two chosen locations. Specify woe_id and find out common trends. 
<br>

![11](https://user-images.githubusercontent.com/26208598/48213083-edcac300-e374-11e8-849e-c707b46108a1.PNG)

<br>

### Popular Retweets


Choose a keyword and find out most popular tweets in a subject.
<br>

![12](https://user-images.githubusercontent.com/26208598/48213091-f15e4a00-e374-11e8-863c-a76014c644a2.PNG)

<br>


## TOOLS, MODULES & TECHNIQUES

##### Python – web development:
Flask | Tweepy | Oauthlib | Pickle

##### Databases
MongoDB | mlab | Sqlite

##### Python – Text Processing
nltk | re 

##### Python – LSTM:
keras | tensorflow | numpy | scikit-learn | h5py

##### Web Development:
HTML | CSS | Bootstrap | Materialize | Conda | Heroku

<br>

Thank you,

Lukasz Malucha
