from flask import Flask
from .routes.user import user
from .routes.index import index
from .routes.movies import movie
from .config import Config
from .extensions import db, migrate, login_manager
from .logging_config import setup_logging


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(index)
    app.register_blueprint(user)
    app.register_blueprint(movie)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # LOGIN MANAGER
    login_manager.login_view = 'user.login'
    login_manager.login_message = 'Для доступа к этой странице требуется авторизация.'
    login_manager.login_message_category = 'info'

    setup_logging()

    with app.app_context():
        db.create_all()

    return app
