from flask import Blueprint, render_template, request, jsonify
import requests

from ..models.movie import Movie, search_movies

KINOPOISK_API_KEY = 'FKDDZFV-JESMS6N-G1G9PXA-821S381'
movie = Blueprint('movie', __name__, url_prefix='/movie')


@movie.route('/', methods=['GET', 'POST'])
def movie_list():
    movies_query = Movie.query.all()
    movies = []
    if request.method == 'POST':
        title = request.form.get('title')
        if title:
            movies = search_movies(title, KINOPOISK_API_KEY)
    return render_template('movies/movies_list.html', movies_query=movies_query, movies=movies)


@movie.route('/<int:movie_id>')
def movie_detail(movie_id):
    return render_template('movies/movie_detail.html', movie_id=movie_id)


@movie.route('/search', methods=['GET'])
def movie_search():
    title = request.args.get('title')
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    movies = search_movies(title, KINOPOISK_API_KEY)
    if not movies:
        return jsonify({'error': 'No movies found'})

    return jsonify(movies)
