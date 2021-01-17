import pickle

import numpy as np
import pandas as pd

from flask import Flask, render_template, request

from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Data reading
movie_dataset = pd.read_csv(r'testset_movies.csv')
movieclips = pd.read_csv(r'testset_ids.csv')
array = np.load(r'test_emb.npy')

movies = movie_dataset['movieId'].to_list()
titles = movie_dataset['title'].to_list()


youtube_clips = dict()
for m_id in movies:
    clip_str = movieclips[movieclips['movieId'] == m_id].movieclipId.to_list()
    youtube_clips[m_id] = ["".join(c.split("_")[1:]) for c in clip_str]

# drop the last part of title with the year: "(2005)"
titles_clipped = [" ".join(t.split(" ")[:-1]).lower() for t in titles]

dico_movie = dict(enumerate(movies))

dico_movie = {k: v for (v, k) in dico_movie.items()}


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search')
def search():
    query = request.args['search']

    try:
        if int(query) in movies:
            q_id = int(query)
            q_title = titles[dico_movie[q_id]]

    #  if we can't cast to int, it's a string:
    except:
        query = query.lower()

        # just title without year:
        if query in titles_clipped:
            q_title = titles[titles_clipped.index(query)]
            q_id = movies[titles_clipped.index(query)]

        # full title with year:
        elif query in titles:
            q_title = query
            q_id = movies[titles.index(query)]

        else:
            print("TITLE NOT FOUND...... use first movie:")
            q_id = 0
            q_title = titles[0]

    similarity = cosine_similarity(array, array[dico_movie[q_id]].reshape(1, -1)).squeeze()

    most = np.argsort(similarity)[::-1][1:101]

    score = np.sort(similarity)[::-1][1:101]

    results = [(titles[i], np.round(s*1000)/10., movies[i], youtube_clips[movies[i]]) for i, s in zip(most, score)]

    return render_template('search_result.html', res=results, title=q_title)



if __name__ == '__main__':
    app.run(debug=True)
