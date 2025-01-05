from flask import Blueprint, render_template, request, jsonify
from ..models.posts import Post, search_movies_by_title, search_movie_by_id, DetailMovie, PostMovie

movie = Blueprint('movie', __name__, url_prefix='/movie')


@movie.route('/', methods=['GET'])
def movie_list():
    movies_query = Post.query.all()
    movies = []
    for movie in movies_query:
        json = search_movie_by_id(movie.api_id)
        movies.append(PostMovie(json))

    return render_template('movies/movies_list.html', movies=movies)


@movie.route('/<int:post_id>')
def movie_detail(post_id):
    api_id = Post.query.get(post_id).api_id
    result = search_movie_by_id(api_id)
    movie = DetailMovie(result)
    return render_template('movies/movie_detail.html', movie=movie)


@movie.route('/search', methods=['GET'])
def movie_search():
    title = request.args.get('title')
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    movies = search_movies_by_title(title)
    if not movies:
        return jsonify({'error': 'No movies found'})

    return jsonify(movies)
