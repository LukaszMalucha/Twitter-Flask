# -*- coding: utf-8 -*-


import pandas as pd
import re


dataset = pd.read_csv('dataset.csv')


################################################################## Twitter text #######################################

tweet = re.sub('[^a-zA-Z]',                                  ## not the letters a-z/A-Z..
                ' '              ,                            ## space to separate characters    
                dataset['text'][0]     )                    ## in a first review....
                
              
tweet = tweet.lower()      


## get rid of irrelevant and stemming words:
import nltk   
nltk.download('stopwords')          ## stopwords list
from nltk.corpus import stopwords 

## getting the root of every word (stemming):
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()




#### INITIALIZE FOR LOOP:

corpus = []
for i in range(0,200):
        tweet = re.sub('[^a-zA-Z]',' ',dataset['text'][i])    ## all the indexes
        tweet = tweet.lower()
        tweet = tweet.split() 
        ps = PorterStemmer()
        tweet = [ps.stem(word) for word in tweet if not word in set(stopwords.words('english'))]
        tweet = ' '.join(tweet)
        corpus.append(tweet)
  
      
text_df = pd.DataFrame({'tweet':corpus}) 

dataset['text'] =   text_df['tweet']     
        
################################################################## Twitter date #######################################     
        
date_df = pd.DataFrame(dataset.date.str.split(' ', expand=True).values, columns=['weekday', 'month', 'day', 'time'])

dataset['weekday'] = date_df['weekday']   
dataset['month'] = date_df['month']           
dataset['day'] = date_df['day']           
dataset['time'] = date_df['time']       
        
        
dataset = dataset.drop(['date'], axis=1)
 
        
        
################################################################ Twitter author ########################################        
        
dataset['author'] = dataset['author'].str.replace('"', '')   






















     
        
        
        
        
        
        