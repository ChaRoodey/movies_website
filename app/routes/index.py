from flask import Blueprint, render_template


index = Blueprint('index', __name__, url_prefix='/index')

@index.route('/')
def home_page():
    return render_template('index/index.html')


