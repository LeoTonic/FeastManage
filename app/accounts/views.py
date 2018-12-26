from flask import Blueprint, flash, render_template, redirect, url_for, request, current_app, abort
from flask_login import login_user, logout_user, login_required, current_user
from app import app_version
from app.models import User
from .forms import LoginForm

accounts = Blueprint('accounts', __name__)


@accounts.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if not current_user.is_administrator:
        abort(403)

    page = request.args.get('page', 1, type=int)
    pagination = User.query.filter(User.login != 'admin').paginate(
        page, per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False)
    context = dict()
    context['users'] = pagination.items
    context['pagination'] = pagination
    context['app_version'] = app_version
    return render_template('accounts/index.html', context=context)


@accounts.route('/login', methods=['GET', 'POST'])
# def login():
#     # ВРЕМЕННОЕ РЕШЕНИЕ ДЛЯ ДЕБАГА
#     user = User.query.filter_by(login='admin').first()
#     if user is not None:
#         login_user(user, True)
#         return redirect(url_for('performers.index'))
#     else:
#         abort(500)
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
