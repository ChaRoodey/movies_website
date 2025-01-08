import os


class Config(object):
    APPNAME = 'app'
    ROOT = os.path.abspath(APPNAME)
    SERVER_PATH = os.path.join(ROOT, 'static/upload')

    USER = os.environ.get('POSTGRES_USER', 'vladev')
    PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'qazwsx')
    HOST = os.environ.get('POSTGRES_HOST', '127.0.0.1')
    PORT = os.environ.get('POSTGRES_PORT', 5532)
    DB = os.environ.get('POSTGRES_DB', 'movies_db')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    SECRET_KEY = 'fnenwhg67dsnjkn34gnhrbuwunvjdsbuy78v8s32kjr'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
