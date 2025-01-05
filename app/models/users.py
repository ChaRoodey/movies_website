from datetime import datetime, timezone
from ..extensions import db
from .posts import Post


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movies = db.relationship(Post, backref='author')
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    avatar = db.Column(db.String(255))
    name = db.Column(db.String(255))
