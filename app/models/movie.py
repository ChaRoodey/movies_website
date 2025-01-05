import requests
from datetime import datetime, timezone
from ..extensions import db


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    api_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    post_creation_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))


def search_movies(title, api_key):
    url = f'https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=10&query={title}'
    headers = {
        "accept": "application/json",
        'X-API-Key': api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['docs']
    return None
