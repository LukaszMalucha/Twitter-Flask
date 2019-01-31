# -*- coding: utf-8 -*-

import keras
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM
import pandas as pd
import numpy as np
from keras.preprocessing.text import Tokenizer
from sklearn.model_selection import train_test_split
from keras.models import load_model 

import re
import nltk
import pickle
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

tweets = pd.read_csv('Tweets.csv')
data = tweets[['text','airline_sentiment']]


## Preprocess data
data['text'] = data['text'].apply(lambda x: x.lower())
data['text'] = data['text'].apply((lambda x: re.sub('[^a-zA-z0-9\s]','',x)))
data['text'] = data['text'].apply((lambda x: x.split()))
data['text'] = data['text'].apply(lambda x: [ps.stem(word) for word in x if not word in set(stopwords.words('english'))])
data['text'] = data['text'].apply((lambda x: ' '.join(x)))

## Tokenizer
max_fatures = 5000
tokenizer = Tokenizer(num_words=max_fatures, split=' ')
tokenizer.fit_on_texts(data['text'].values)

with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

X = tokenizer.texts_to_sequences(data['text'].values)
X = pad_sequences(X)


## Model Architecture
embed_dim = 256
lstm_out = 392

model = Sequential()
model.add(Embedding(max_fatures, embed_dim,input_length = X.shape[1]))
model.add(Dropout(0.5))
model.add(LSTM(lstm_out, dropout=0.3, recurrent_dropout=0.3))
model.add(Dense(3,activation='softmax'))
model.compile(loss = 'categorical_crossentropy', optimizer='adam',metrics = ['accuracy'])

Y = pd.get_dummies(data['airline_sentiment']).values

X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.33)



X_val = X_train[:500]
Y_val = Y_train[:500]

partial_X_train = X_train[500:]
partial_Y_train = Y_train[500:]

batch_size = 512


## Model Apply

model.fit(partial_X_train, 
                    partial_Y_train, 
                    epochs = 10, 
                    batch_size=batch_size, 
                    validation_data=(X_val, Y_val))


## Model Save

model.save('sentiment_model.h5') 

model_json = model.to_json()
with open("sentiment_model.json", "w") as json_file:
    json_file.write(model_json)
    
model.save_weights("sentiment_model.h5")
print("Saved model to disk")    
 

################################################################################

## Single Prediction Test
# tweety = 'love hate love'
# tweety = re.sub('[^a-zA-Z]',' ',tweety)
# tweety = tweety.lower()
# tweety = tweety.split()
# tweety = [ps.stem(word) for word in tweety if not word in set(stopwords.words('english'))]
# tweety = tokenizer.texts_to_sequences(tweety)
# tweety = pad_sequences(tweety, maxlen=23, dtype='int32', value=0)
# tweet_pred = model.predict(tweety)





tata = ''
if(np.argmax(tweet_pred) == 0):
    tata = "negative"
elif (np.argmax(tweet_pred) == 1):
    tata = "positive"
else:
    tata = "didi"    





