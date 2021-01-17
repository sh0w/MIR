import pickle

import numpy as np
import pandas as pd

from flask import Flask, render_template, request

from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

NUM_PAGE = 50
NUM_PAGE_PR = 100

# Data reading
data = pd.read_csv(r'testset_movies.csv')
array = np.load(r'test_emb.npy')

movie = data['movieId'].to_list()
title = data['title'].to_list()

dico_movie = dict(enumerate(movie))

dico_movie = {k: v for (v, k) in dico_movie.items()}

@app.route('/')
def home():
    return render_template('home.html')


# @app.route('/articles')
# def all_article():
#     return render_template('articles.html', df=shuffle(df)[:NUM_PAGE_PR])
#
#
# @app.route('/sim_<id_art>')
# def most_sim(id_art):
#     id_art = int(id_art)
#
#     most = np.argsort(array @ array[id_art])[::-1][:NUM_PAGE]
#
#     scores = np.sort(array @ array[id_art])[::-1][:NUM_PAGE]
#
#     arts = [df[i] for i in most]
#
#     res = list(zip(arts, scores))
#
#     return render_template('similar.html', res=res, id_q=id_art)


@app.route('/search')
def search():
    query = request.args['search']

    query = int(query)

    q_title = title[dico_movie[query]]

    similarity = cosine_similarity(array, array[dico_movie[query]].reshape(1, -1)).squeeze()

    most = np.argsort(similarity)[::-1][1:101]

    score = np.sort(similarity)[::-1][1:101]


    res = [(title[i], s, movie[i]) for i, s in zip(most, score)]

    return render_template('search_result.html', res=res, title=q_title)


@app.template_filter()
def format_score(value):
    value = float(value)
    return "{:,.0%}".format(value)


# @app.route('/charts/')
# def line_route():
#     return render_template('charts.html', chart=chart)


if __name__ == '__main__':
    app.run(debug=True)
