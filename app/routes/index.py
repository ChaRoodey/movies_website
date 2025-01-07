import logging

from flask import Blueprint, render_template
from flask_login import current_user

index = Blueprint('index', __name__, url_prefix='/index')
logger = logging.getLogger(__name__)

@index.route('/')
def home_page():
    logger.info('home_page endpoint')
    if current_user.is_authenticated:
        return render_template('index/index_auth.html')
    return render_template('index/index_unauth.html')


