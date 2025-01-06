from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import current_user
from ..models.posts import Post, search_movie, DetailMovie, Genre, Actor
from ..extensions import db


movie = Blueprint('movie', __name__, url_prefix='/movie')


@movie.before_request
def require_login():
    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))


@movie.route('/', methods=['GET'])
def movie_list():
    movies_query = Post.query.filter_by(post_author=current_user.id).order_by(Post.post_creation_date.desc()).all()
    return render_template('movies/movies_list.html', movies=movies_query)


@movie.route('/add', methods=['POST'])
def add_movie():
    movie_api_id = request.args.get('movie_id')
    if not movie_api_id:
        return jsonify({'message': 'ID фильма не передан!'}), 400

    result = search_movie(movie_id=movie_api_id)
    if not result:
        return jsonify({'message': 'Фильм не найден!'}), 404

    try:
        title = result.get('name')
        post_author = current_user.id
        description = result.get('description')
        year = result.get('year')
        movie_type = result.get('type')
        poster = result.get('poster', {}).get('url', 'static/img/logo.jpg')

        genre = result.get('genres', [])
        genre_names = [genre.get('name') for genre in genre]

        persons = result.get('persons', [])
        top_actors = persons[:5]
        actors_data = [(actor.get('id'), actor.get('name'), actor.get('photo')) for actor in top_actors]

        new_movie = Post(
            movie_api_id=movie_api_id,
            post_author=post_author,
            title=title,
            description=description,
            year=year,
            type=movie_type,
            poster=poster,
            status=1,
            rating=1
        )

        db.session.add(new_movie)
        db.session.flush()

        for genre_name in genre_names:
            existing_genre = Genre.query.filter_by(name=genre_name).first()
            if not existing_genre:
                existing_genre = Genre(name=genre_name)
                db.session.add(existing_genre)
            new_movie.genres.append(existing_genre)


        for actor_api_id, name, photo in actors_data:
            existing_actor = Actor.query.filter_by(actor_api_id=actor_api_id).first()
            if not existing_actor:
                existing_actor = Actor(actor_api_id=actor_api_id, name=name, photo=photo)
                db.session.add(existing_actor)
            new_movie.actors.append(existing_actor)

        db.session.commit()

        return jsonify({"message": "Фильм успешно добавлен!"}), 200
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({"message": "Ошибка при добавлении фильма!"}), 500


@movie.route('/<int:api_id>')
def movie_detail(api_id):
    post = Post.query.filter_by(movie_api_id=api_id).first()
    if not post:
        return jsonify({'message': 'Фильм не найден!'}), 404

    genres = [genre.name for genre in post.genres]
    actors = post.actors
    movie = DetailMovie(post=post, actors=actors, genres=genres)
    actors_info = list(zip(movie.actor_name, movie.actor_photo))

    return render_template('movies/movie_detail.html', movie=movie, actors_info=actors_info)


@movie.route('/search', methods=['GET'])
def movie_search():
    title = request.args.get('title')
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    movies = search_movie(movie_title=title)
    if not movies:
        return jsonify({'error': 'No movies found'})

    movie_results = []
    for movie in movies:
        is_added = Post.query.filter_by(movie_api_id=movie.get('id'), post_author=current_user.id).first()
        movie['is_added'] = True if is_added else False
        movie_results.append(movie)

    return jsonify(movie_results), 200
