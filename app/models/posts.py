import requests
from datetime import datetime, timezone
from ..extensions import db


KINOPOISK_API_KEY = 'FKDDZFV-JESMS6N-G1G9PXA-821S381'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    api_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    post_creation_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))


class PostMovie:
    def __init__(self, data=None):
        if data:
            self.movie_id = data.get('id')
            self.type = data.get('type')
            self.title = data.get('name')
            self.year = data.get('year')
            self.poster = data.get('poster').get('url')


class DetailMovie:
    def __init__(self, data=None):
        if data:
            self.type = data.get('type')
            self.title = data.get('name')
            self.description = data.get('description')
            self.year = data.get('year')
            self.poster = data.get('poster').get('url')
            self.genres = [genre.get('name') for genre in data.get('genres')]
            self.actor_name = [person.get('name') for person in data.get('persons')[:5]]
            self.actor_photo = [person.get('photo') for person in data.get('persons')[:5]]


def search_movie_by_id(movie_id):
    url = f'https://api.kinopoisk.dev/v1.4/movie/{movie_id}'
    headers = {
        "accept": "application/json",
        'X-API-Key': KINOPOISK_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


def search_movies_by_title(title):
    url = f'https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=10&query={title}'
    headers = {
        "accept": "application/json",
        'X-API-Key': KINOPOISK_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['docs']
    return None
