# -*- coding: utf-8 -*-
"""Final Model

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hHheFYmtFrYHbAQi0XwJmt4cQovmMWS2
"""

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from tensorflow import keras

model1 = keras.models.load_model(
    '/Users/ydonia/Documents/Junior Year/Semester 1/AIM/AIM Project/sentiment.h5')
model2 = keras.models.load_model(
    '/Users/ydonia/Documents/Junior Year/Semester 1/AIM/AIM Project/genre.h5')
# print(f"Model 1: {model1.summary()}")
# print(f"Model 2: {model2.summary()}")
# model1.summary()
# model2.summary()


# Loads in models

rtDF = pd.read_csv(
    "/Users/ydonia/Documents/Junior Year/Semester 1/AIM/AIM Project/cleaned_RT_Dataset.csv")

processed_critics = []
wordAmt = 0
# for each review, tokenize, and remove stopwords
for review in rtDF['new_critics_consensus']:
    strReview = str(review)
    strippedWords = strReview.strip()
    wordAmt += len(strippedWords.split(" "))
    # join the tokenized & stop word removed words and append to new list
    processed_critics.append(strippedWords)
# assign that list to that data frame column of 'new description'
rtDF['new_critics_consensus'] = processed_critics
# print(wordAmt)

rtDF.head()

rtDF.dropna()
Model1_Critics_Test = rtDF['new_critics_consensus']
num_words = 55000

tokenizer = Tokenizer(num_words=num_words)
tokenizer.fit_on_texts(Model1_Critics_Test)
M1_train_seq = pd.Series(tokenizer.texts_to_sequences(Model1_Critics_Test))

M1_train_pad = pad_sequences(M1_train_seq, maxlen=256)

M1_predictions = model1.predict(M1_train_pad)

# print(type(M1_predictions))
M1_predictions = M1_predictions.tolist()
# print(M1_predictions)

newCol = []
for num in M1_predictions:
    revNum = num[0]
    newCol.append(revNum)

rtDF['Sentiment'] = newCol
# rtDF.head()


Model2_Test = rtDF['new_description']
num_words = 55000

tokenizer = Tokenizer(num_words=num_words)
tokenizer.fit_on_texts(Model2_Test)

M2_train_seq = pd.Series(tokenizer.texts_to_sequences(Model2_Test))

M2_train_pad = pad_sequences(M2_train_seq, maxlen=256)

M2_predict = model2.predict(M2_train_pad)

M2_predict_round = np.round(M2_predict, 2)
predDF = pd.DataFrame(M2_predict_round)

predDF = predDF.rename(columns={0: 'P_Romance', 1: 'P_Drama', 2: 'P_Adventure', 3: 'P_Fantasy', 4: 'P_Mystery',
                       5: 'P_Horror', 6: 'P_Comedy', 7: 'P_Family', 8: 'P_Action', 9: 'P_Sci-Fi', 10: 'P_Thriller', 11: 'P_Adult'})

# predDF.head()

rtDF = pd.concat([rtDF, predDF], axis=1)
pd.set_option('display.max_columns', None)
# print(rtDF.head())

sentCutOff = .95
genreCutOff = .70

# USER QUIZ

genres = ["Comedy", "Drama", "Romance", "Sci-Fi", "Thriller",
          "Horror", "Fantasy", "Action", "Mystery", "Family", "Adult", "Adventure"]
# LAST 3 GENRES I ADDED ARE NEW AND HAVE NOT BEEN ACCOUNTED FOR YET NEED TO CHANGE

scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

"""Make lists for the genres and the score for each genre, and combine into a list of tuples. """

questions = [
    ("Do you want a lighthearted movie? ", ("Comedy", 1),
     ("Romance", 1), ("Family", 1), ("Fantasy", 0.5)),
    ("Do you want a movie that's gonna get you thinking? ",
     ("Mystery", 1), ("Thriller", 1), ("Drama", 0.5), ("Sci-Fi", 0.5)),
    ("Do you want a movie that's gonna scare you? ", ("Horror", 1),
     ("Thriller", 0.5), ("Sci-Fi", 0.5), ("Mystery", 0.5), ("Adult", 0.5)),
    ("Do you want a movie that's gonna make you laugh? ",
     ("Comedy", 1), ("Romance", 0.5), ("Action", 0.5)),
    ("Do you want an action packed movie? ", ("Action", 1),
     ("Adventure", 1), ("Fantasy", 0.5), ("Sci-Fi", 0.5))
]

"""Make questions with movie tags associated with them."""

for question in questions:
    answer = input(question[0])
    if (answer.upper() == "YES") or (answer.upper() == "Y"):
        # ignore the first element (question) of the list
        for tag, weight in question[1:]:
            # find the corresponding tag in the genres list and add the weight
            index = genres.index(tag)
            scores[index] = scores[index] + weight
        # print(genres)
        # print(scores)
    elif (answer.upper() == "NO") or (answer.upper() == "N"):  # keep the arrays the same
        continue

# find the genre with the highest score in the list
max_index = scores.index(np.max(scores))
# print(index)
inputGenre = genres[max_index]

# inputGenre = 'Comedy'
genre = f"P_{inputGenre}"
print(f"Here are the top 10 {inputGenre} movies for you!")

movieTitle = []
parallelGenre = []
comedyScores = []
sentimentScores = []

for index_row, row_series in rtDF.iterrows():
    sentScore = rtDF.at[index_row, 'Sentiment']
    genreScore = rtDF.at[index_row, genre]
    if(sentScore < sentCutOff):
        continue
    if(genreScore < genreCutOff):
        continue
    movieTitle.append(rtDF.at[index_row, 'movie_title'])
    parallelGenre.append(rtDF.at[index_row, 'genres'])
    comedyScores.append(rtDF.at[index_row, genre])
    sentimentScores.append(sentScore)

# pd.set_option('display.max_columns', None)
resultDF = pd.DataFrame(movieTitle)
resultDF = resultDF.rename(columns={0: 'Movie Title'})

genreDF = pd.DataFrame(parallelGenre)
resultDF = pd.concat([resultDF, genreDF], axis=1)
resultDF = resultDF.rename(columns={0: 'Genres'})

comedyDF = pd.DataFrame(comedyScores)
resultDF = pd.concat([resultDF, comedyDF], axis=1)
resultDF = resultDF.rename(columns={0: f'{inputGenre} Score'})

sentDF = pd.DataFrame(sentimentScores)
resultDF = pd.concat([resultDF, sentDF], axis=1)
resultDF = resultDF.rename(columns={0: f'Sentiment Score'})

for index_row, row_series in resultDF.iterrows():
    genreList = resultDF.at[index_row, 'Genres']
    if inputGenre not in genreList:
        resultDF = resultDF.drop(index_row)
# print("Here are your recommended movies!")
print(resultDF.head(10))


# reset scores for quiz
i = 0
while i < len(scores):
    scores[i] = 0
    i = i + 1
