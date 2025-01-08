import logging

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import current_user
from ..models.posts import Post, search_movie, DetailMovie, Genre, Actor, status_id_to_str
from ..extensions import db


movie = Blueprint('movie', __name__, url_prefix='/movie')
logger = logging.getLogger(__name__)


@movie.before_request
def require_login():
    if not current_user.is_authenticated:
        logger.debug('User not logged in, redirecting to login')
        return redirect(url_for('user.login'))


@movie.route('/', methods=['GET'])
def movie_list():
    logger.info('Movie list endpoint')
    title = request.args.get('title', None)
    year = request.args.get('year', None)
    status = request.args.get('status', None)
    logger.debug(f'Movie_list setup args: {title=} {status=} {year=}')

    movies_query = Post.query.filter_by(post_author=current_user.id)

    if title:
        title = str(title).title()
        movies_query = movies_query.filter(Post.title.like(f"%{title}%"))
    if year:
        movies_query = movies_query.filter(Post.year == year)
    if status:
        movies_query = movies_query.filter(Post.status == status)

    movies_query = movies_query.order_by(Post.post_creation_date.desc()).all()

    filters = []
    if status:
        status = status_id_to_str(status)
        filters.append({'key': 'status', 'value': status, 'label': f'Статус: {status}'})
    if year:
        filters.append({'key': 'year', 'value': year, 'label': f'Год: {year}'})
    if title:
        filters.append({'key': 'title', 'value': title, 'label': f'Название: {title}'})

    logger.debug(f'Movie_list filters result: {filters}')

    current_args = request.args.to_dict()

    logger.debug(f'Movie_list current args: {current_args}')

    return render_template('movies/movies_list.html', movies=movies_query, filters=filters, current_args=current_args)


@movie.app_template_filter('dict_without')
def dict_without(d, key):
    logger.debug(f'Movie_list filter: {d}')
    if key in d:
        d = d.copy()
        d.pop(key)
        logger.debug(f'Movie_list filter result: {d}')
    return '&'.join([f'{k}={v}' for k, v in d.items()])


@movie.route('/add', methods=['POST'])
def add_movie():
    logger.info('Add_movie endpoint')
    movie_api_id = request.args.get('movie_id')
    logger.debug(f'Movie_api_id: {movie_api_id}')

    if not movie_api_id:
        logger.error('Movie id not provided, redirecting to add_movie')
        return jsonify({'message': 'ID фильма не передан!'}), 400

    result = search_movie(movie_id=movie_api_id)
    logger.debug(f'Movie_api_id: {movie_api_id} result: {result}')

    if not result:
        logger.error('Movie not found in api database, redirecting to add_movie')
        return jsonify({'message': 'Фильм не найден!'}), 404

    try:
        title = result.get('name')
        post_author = current_user.id
        description = result.get('description')
        year = result.get('year')
        movie_type = result.get('type')
        poster = result.get('poster', {}).get('url', 'static/img/logo.jpg')
        rating = result.get('rating').get('imdb')

        genre = result.get('genres', [])
        genre_names = [genre.get('name') for genre in genre]
        logger.debug(f'Movie_api_id: {movie_api_id} result: {genre_names}')

        persons = result.get('persons', [])
        top_actors = persons[:5]
        actors_data = [(actor.get('id'), actor.get('name'), actor.get('photo')) for actor in top_actors]
        logger.debug(f'Movie_api_id: {movie_api_id} actors: {actors_data}')

        new_movie = Post(
            movie_api_id=movie_api_id,
            post_author=post_author,
            title=title,
            description=description,
            year=year,
            type=movie_type,
            poster=poster,
            status=1,
            rating=rating
        )

        db.session.add(new_movie)
        db.session.flush()

        for genre_name in genre_names:
            existing_genre = Genre.query.filter_by(name=genre_name).first()
            if not existing_genre:
                existing_genre = Genre(name=genre_name)
                db.session.add(existing_genre)
                logger.debug(f'{genre_name=} added to db')
            new_movie.genres.append(existing_genre)


        for actor_api_id, name, photo in actors_data:
            existing_actor = Actor.query.filter_by(actor_api_id=actor_api_id).first()
            if not existing_actor:
                existing_actor = Actor(actor_api_id=actor_api_id, name=name, photo=photo)
                db.session.add(existing_actor)
                logger.debug(f'{actor_api_id=}, {name=}, {photo=} added to db')
            new_movie.actors.append(existing_actor)

        db.session.commit()
        logger.info(f'Movie added succesfully: {movie_api_id}')
        return jsonify({"message": "Фильм успешно добавлен!"}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f'Movie add error result: {e}')
        return jsonify({"message": "Ошибка при добавлении фильма!"}), 500


@movie.route('/<int:api_id>')
def movie_detail(api_id):
    logger.info('Movie detail endpoint')
    post = Post.query.filter_by(movie_api_id=api_id).first()
    if not post:
        logger.error(f'Movie bot found in db by {api_id=}')
        return jsonify({'message': 'Фильм не найден!'}), 404

    genres = [genre.name for genre in post.genres]
    actors = post.actors
    movie = DetailMovie(post=post, actors=actors, genres=genres)
    actors_info = list(zip(movie.actor_name, movie.actor_photo))
    logger.info(f'Movie detail result: {movie}')
    return render_template('movies/movie_detail.html', movie=movie, actors_info=actors_info)


@movie.route('/search', methods=['GET'])
def movie_search():
    logger.info('Movie search endpoint')
    title = request.args.get('title')
    if not title:
        logger.error(f'Movie title not provided {title=}, redirecting to add_movie')
        return jsonify({'error': 'Title is required'}), 400

    movies = search_movie(movie_title=title)
    if not movies:
        logger.error(f'Movie not found in api db: {title}')
        return jsonify({'error': 'No movies found'})

    movie_results = []
    for movie in movies:
        is_added = Post.query.filter_by(movie_api_id=movie.get('id'), post_author=current_user.id).first()
        movie['is_added'] = True if is_added else False
        movie_results.append(movie)

    logger.debug(f'Search result {movie_results=}')
    return jsonify(movie_results), 200


@movie.route('/change_status', methods=['POST'])
def change_status():
    logger.info('Movie change endpoint')
    data = request.get_json()
    movie_id = data.get('movie_id')
    status = data.get('status')

    movie = Post.query.filter_by(id=movie_id, post_author=current_user.id).first()
    if not movie:
        logger.error(f'Movie not found in api db: {movie_id=}')
        return jsonify({'success': False, 'message': 'Фильм не найден'}), 404

    try:
        movie.status = status
        db.session.commit()
        logger.info(f'Movie status changed to {status}')
        return jsonify({'success': True}), 200
    except Exception as e:
        logger.error(f'Movie status change failed: {e}')
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
