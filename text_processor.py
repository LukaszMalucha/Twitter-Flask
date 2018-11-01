# -*- coding: utf-8 -*-


import pandas as pd
import re


dataset = pd.read_csv('dataset.csv')


## Twitter text

tweet = re.sub('[^a-zA-Z]',                                  ## not the letters a-z/A-Z..
                ' '              ,                            ## space to separate characters    
                dataset['text'][0]     )                    ## in a first review....
                
              
tweet = tweet.lower()      


## get rid of irrelevant and stemming words:
import nltk   
nltk.download('stopwords')          ## stopwords list
from nltk.corpus import stopwords
tweet = tweet.split()          ## sentence to the list        

## getting the root of every word (stemming):
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
tweet = [ps.stem(word) for word in tweet if not word in set(stopwords.words('english'))]  ##keep the words that are not in a stopwords
        ##stemming                                     ## set makes algorithm faster


tweet = ' '.join(tweet)               ## join he words with a space