import logging
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required
from ..models.users import User
from ..extensions import bcrypt, db
from ..forms import RegistrationForm, LoginForm


user = Blueprint('user', __name__, url_prefix='/user')
logger = logging.getLogger(__name__)


@user.route('/register', methods=['GET', 'POST'])
def register():
    logger.info('Register endpoint')
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            logger.info(f'User registered successfully {form.username.data}')
            return redirect('/user/login')
        except Exception as e:
            logger.error(f'User add error result: {e}')
            db.session.rollback()
            # flash(f'Ошибка при регистрации', 'danger')
    return render_template('/user/register.html', form=form)


@user.route('/login', methods=['GET', 'POST'])
def login():
    logger.info('Login endpoint')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            logger.info(f'User logged in successfully {form.username.data}')
            return redirect(next_page) if next_page else redirect(url_for('movie.movie_list'))
        else:
            logger.info(f'User login failed {form.username.data}')
            return 'Некорректный никнейм/пароль'

    return render_template('/user/login.html', form=form)


@login_required
@user.route('/profile')
def profile():
    logger.info('Profile endpoint')
    return render_template('/user/profile.html')


@user.route('/logout')
def logout():
    logger.info('Logout endpoint')
    logout_user()
    return redirect('/index')
