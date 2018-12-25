from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required
from app import app_version
from app.models import User
from .forms import LoginForm

accounts = Blueprint('accounts', __name__)


@accounts.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user is not None:
            if user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                next_var = request.args.get('next')
                if next_var is None or not next_var.startswith('/'):
                    next_var = url_for('performers.index')
                return redirect(next_var)
            else:
                flash(u'Неверный пароль')
        else:
            flash(u'Пользователь не найден')
    context = dict()
    context['form'] = form
    context['app_version'] = app_version
    return render_template('accounts/login.html', context=context)


@accounts.route('/logout')
@login_required
def logout():
    flash(u'Вы вышли из системы')
    logout_user()
    return redirect(url_for('performers.index'))
