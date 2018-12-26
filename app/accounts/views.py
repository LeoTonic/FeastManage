from flask import Blueprint, flash, render_template, redirect, url_for, request, current_app, abort
from flask_login import login_user, logout_user, login_required, current_user
from app import app_version, db
from app.models import User
from .forms import LoginForm, PasswordForm, AdminProfileForm

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
            # проверка первого входа в приложение
            if user.has_password:
                if user.verify_password(form.password.data):
                    login_user(user, form.remember_me.data)
                    # next_var = request.args.get('next')
                    # if next_var is None or not next_var.startswith('/'):
                    #     next_var = url_for('performers.index')
                    return redirect(url_for('performers.index'))
                else:
                    flash(u'Неверный пароль')
            else:
                return redirect(url_for('.setpassword', user_id=user.id))
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


@accounts.route('/setpassword/<int:user_id>', methods=['GET', 'POST'])
def setpassword(user_id):
    """ Установка пароля пользователю """
    form = PasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=user_id).first()
        if user is not None:
            if user.has_password:
                flash(u'Данному пользователю уже установлен пароль')
            else:
                user.password = form.password.data
                user.has_password = True
                db.session.add(user)
                db.session.commit()
                flash(u'Пароль сохранен')
        else:
            flash(u'Пользователь не найден')
        return redirect(url_for('.index'))
    context = dict()
    context['form'] = form
    context['app_version'] = app_version
    return render_template('accounts/setpassword.html', context=context)


@accounts.route('/resetpassword', methods=['POST'])
def resetpassword():
    """ Сброс пароля """
    return None


@accounts.route('/newuser', methods=['GET', 'POST'])
def newuser():
    """ Регистрация нового пользователя """
    form = AdminProfileForm(None)
    if form.validate_on_submit():
        user = User()
        user.login = form.login.data
        user.name_first = form.name_first.data
        user.name_last = form.name_last.data
        user.name_middle = form.name_middle.data
        user.email = form.email.data
        user.role = form.role.data
        user.company = form.company.data
        user.phone1 = form.phone1.data
        user.phone2 = form.phone2.data
        user.fax = form.fax.data
        db.session.add(user)
        db.session.commit()
        flash(u'Пользователь успешно создан')
        return redirect(url_for('.index'))
    context = dict()
    context['form'] = form
    context['app_version'] = app_version
    return render_template('accounts/profile.html', context=context)


@accounts.route('/user/<int:user_id>', methods=['GET', 'POST'])
def edituser(user_id):
    """ Редактирование пользователя """
    return None
