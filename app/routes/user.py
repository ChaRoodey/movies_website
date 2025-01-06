from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required

from ..models.users import User
from ..extensions import bcrypt, db
from ..forms import RegistrationForm, LoginForm

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/user/login')
        except Exception as e:
            print(str(e))
            db.session.rollback()
            # flash(f'Ошибка при регистрации', 'danger')
    return render_template('/user/register.html', form=form)


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('movie.movie_list'))
        else:
            return 'Некорректный никнейм/пароль'

    return render_template('/user/login.html', form=form)


@login_required
@user.route('/profile')
def profile():
    return 'Профиль'


@user.route('/logout')
def logout():
    logout_user()
    return redirect('/index')
