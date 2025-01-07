import requests
from datetime import datetime, timezone
from ..extensions import db


KINOPOISK_API_KEY = 'FKDDZFV-JESMS6N-G1G9PXA-821S381'
HEADERS = {
    "accept": "application/json",
    'X-API-Key': KINOPOISK_API_KEY
}


post_actors = db.Table(
    'post_actors',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id', ondelete='CASCADE'), primary_key=True),
)


post_genres = db.Table(
    'post_genres',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id', ondelete='CASCADE'), primary_key=True),
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    movie_api_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    poster = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    actors = db.relationship('Actor', secondary=post_actors, backref='actor_posts')
    genres = db.relationship('Genre', secondary=post_genres, backref='genres_posts')
    status = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    post_creation_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actor_api_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    photo = db.Column(db.String, nullable=False)


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


class DetailMovie:
    def __init__(self, post=None, actors=None, genres=None):
            self.type = post.type
            self.title = post.title
            self.description = post.description
            self.status = post.status
            self.rating = post.rating
            self.year = post.year
            self.poster = post.poster
            self.genres = genres
            self.actor_name = [actor.name for actor in actors]
            self.actor_photo = [actor.photo for actor in actors]


def search_movie(movie_id=None, movie_title=None):
    if movie_id:
        url = f'https://api.kinopoisk.dev/v1.4/movie/{movie_id}'
    elif movie_title:
        url = f'https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=10&query={movie_title}'
    else:
        return None

    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200 and movie_id:
        return response.json()
    elif response.status_code == 200 and movie_title:
        return response.json()['docs']
    return None


# def search_movie(title):
#     url = f'https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=10&query={title}'
#     headers = {
#         "accept": "application/json",
#         'X-API-Key': KINOPOISK_API_KEY
#     }
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         return response.json()['docs']
#     return None
# class PostMovie:
#     def __init__(self, data=None):
#         if data:
#             self.movie_id = data.get('id')
#             self.type = data.get('type', 'defType')
#             self.title = data.get('name', None)
#             self.year = data.get('year', None)
#             self.poster = data.get('poster', None).get('url', None)
