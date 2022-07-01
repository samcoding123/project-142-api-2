from flask import Flask, jsonify, request

from storage import all_movies, liked_movies, not_liked_movies
from demographic_filtering import output
from content_filtering import get_recommendations

app = Flask(__name__)

@app.route("/get-article")
def get_movie():
    movie_data = {
        "url": all_movies[0][11],
        "title": all_movies[0][12],
        "text": all_movies[0][13],
        "lang": all_movies[0][14],
        "total_events": all_movies[0][14]
    }
    return jsonify({
        "data": movie_data,
        "status": "success"
    })

@app.route("/liked-article", methods=["POST"])
def liked_movie():
    movie = all_movies[0]
    liked_movies.append(movie)
    all_movies.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/unliked-article", methods=["POST"])
def unliked_movie():
    movie = all_movies[0]
    not_liked_movies.append(movie)
    all_movies.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/popular-aricles")
def popular_movies():
    movie_data = []
    for movie in output:
        _d = {
            "url": movie[0],
            "title": movie[1],
            "text": movie[2],
            "lang": movie[3],
            "total_events": movie[4]
        }
        movie_data.append(_d)
    return jsonify({
        "data": movie_data,
        "status": "success"
    }), 200

@app.route("/recommended-articles")
def recommended_movies():
    all_recommended = []
    for liked_movie in liked_movies:
        output = get_recommendations(liked_movie[4])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    movie_data = []
    for recommended in all_recommended:
        _d = {
            "url": recommended[0],
            "title": recommended[1],
            "text": recommended[2],
            "lang": recommended[3],
            "total_events": recommended[4]
        }
        movie_data.append(_d)
    return jsonify({
        "data": movie_data,
        "status": "success"
    }), 200

if __name__ == "__main__":
  app.run()