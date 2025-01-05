from flask import Blueprint, redirect, render_template

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
            return redirect('/login')
        except Exception as e:
            db.session.rollback()
            # flash(f'Ошибка при регистрации', 'danger')
    return render_template('/user/register.html')


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('/user/login.html')


@user.route('/profile')
def profile():
    pass


@user.route('/logout')
def logout():
    return redirect('/')
