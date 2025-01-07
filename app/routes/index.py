from flask import Blueprint, render_template
from flask_login import current_user

index = Blueprint('index', __name__, url_prefix='/index')

@index.route('/')
def home_page():
    if current_user.is_authenticated:
        return render_template('index/index_auth.html')
    return render_template('index/index_unauth.html')


