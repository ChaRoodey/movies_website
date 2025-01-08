from datetime import datetime, timezone
from ..extensions import db, login_manager
from .posts import Post
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    movies = db.relationship(Post, backref='author')
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    avatar = db.Column(db.String(255))
    name = db.Column(db.String(255))
