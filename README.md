# NLP-Movie-Reccomendation-System
This a movie recommendation system that uses LTSM Neural Networks to classify movies ratings based off of their critic's consensus, and their genres based off of their descriptions. This system then quizzes the user to find out what genre movie the user would most likely want to watch and recommends the best movies of that genre to them.

Model 1:
This model is trained on a dataset with the critics consensus of movies and their IMDB Ratings found on the Keras IMDB Dataset. Once it is trained, I get the model to make its predictions on the Rotten Tomato Dataset (The main one used for the movie database).

Model Summary:
"sequential"
Layer Type       Output Shape        Param #
embedding        (None, None, 100)    2000000 
lstm             (None, 20)           9680
dense            (None, 1)            21
Total Params: 2,009,701
Trainable Params: 2,009,701
Non-Trainable Params : 0

Model 2:
This model is trained on the Kaggle IMDB Dataset with the movie descriptions and their genres. Once it is trained, I get the model to make its predictions on the same Rotten Tomato Dataset. It gives each movie a classification of genres based on percentages.

Model Summary:
"sequential"
Layer Type       Output Shape        Param #
embedding       (None, None, 256)    19200000
lstm            (None, None, 256)    525312
bidirectional   (None, None, 256)    394240
lstm_2          (None, 128)          197120
dense           (None, 64)           8256
dropout         (None, 64)           0
dense_1         (None, 12)           780
Total Params: 20,325,708
Trainable Params: 20,325,708
Non-Trainable Params : 0

main.py:
Here, the two models are connected to make a result dataset. The user is then given a short quiz to try to determine the genre they want. Based on the result genre the quiz determines the user wants to watch, the program then finds movies from the newly classfied dataframe of that same genre, and reccomends the top 10 movies to the user.


Future Goals:
- Improve Accuracy of Models
- Improve quiz to determine genre what user wants
- improve quiz to classify multiple genres
- sort movies based on rating score
