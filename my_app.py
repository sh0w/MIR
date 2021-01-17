import pickle

import numpy as np
import pandas as pd

from flask import Flask, render_template, request

from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Data reading
movie_dataset = pd.read_csv(r'testset_movies.csv')
array = np.load(r'test_emb.npy')

movies = movie_dataset['movieId'].to_list()
titles = movie_dataset['title'].to_list()

dico_movie = dict(enumerate(movies))

dico_movie = {k: v for (v, k) in dico_movie.items()}


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search')
def search():
    query = request.args['search']

    query = int(query)

    q_title = titles[dico_movie[query]]

    similarity = cosine_similarity(array, array[dico_movie[query]].reshape(1, -1)).squeeze()

    most = np.argsort(similarity)[::-1][1:101]

    score = np.sort(similarity)[::-1][1:101]

    results = [(titles[i], s, movies[i]) for i, s in zip(most, score)]

    return render_template('search_result.html', res=results, title=q_title)



if __name__ == '__main__':
    app.run(debug=True)
