from flask import Blueprint, flash, render_template, redirect, url_for, request, current_app, abort, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import app_version, db
from app.models import User, Sort
from .forms import LoginForm, PasswordForm, AdminProfileForm
from . import admin_required

accounts = Blueprint('accounts', __name__)


@accounts.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    page = request.args.get('page', 1, type=int)
    sort_type = request.args.get('stype', Sort.NONE, type=int)
    query = User.query.filter(User.login != 'admin')
    if sort_type == Sort.USER_DESC:
        query = query.order_by(User.name_last.desc()).order_by(User.name_first.desc()).order_by(User.name_middle.desc())
    elif sort_type == Sort.USER:
            query = query.order_by(User.name_last).order_by(User.name_first).order_by(User.name_middle)
    elif sort_type == Sort.CITY:
        query = query.order_by(User.city)
    elif sort_type == Sort.CITY_DESC:
        query = query.order_by(User.city.desc())
    elif sort_type == Sort.COMPANY:
        query = query.order_by(User.company)
    elif sort_type == Sort.COMPANY_DESC:
        query = query.order_by(User.company.desc())
    elif sort_type == Sort.ROLE:
        query = query.order_by(User.role)
    elif sort_type == Sort.ROLE_DESC:
        query = query.order_by(User.role.desc())

    pagination = query.paginate(page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    context = dict()
    context['users'] = pagination.items
    context['pagination'] = pagination
    context['app_version'] = app_version
    context['sort_type'] = sort_type
    context['sort'] = Sort
    return render_template('accounts/index.html', context=context)


@accounts.route('/login', methods=['GET', 'POST'])
# def login():
    # # ВРЕМЕННОЕ РЕШЕНИЕ ДЛЯ ДЕБАГА
    # user = User.query.filter_by(login='admin').first()
    # if user is not None:
    #     login_user(user, True)
    #     return redirect(url_for('performers.index'))
    # else:
    #     abort(500)
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
@login_required
def resetpassword():
    """ Сброс пароля """
    user = User.query.filter_by(login=request.form['login']).first()
    user.has_password = False
    db.session.add(user)
    db.session.commit()
    flash(u'Пароль сброшен')
    return redirect(url_for('.edituser', user_id=user.id))


@accounts.route('/newuser', methods=['GET', 'POST'])
@login_required
@admin_required
def newuser():
    """ Регистрация нового пользователя """
    form = AdminProfileForm(edit=False)
    if form.validate_on_submit():
        user = User()
        user.login = form.login.data
        user.name_first = form.name_first.data
        user.name_last = form.name_last.data
        user.name_middle = form.name_middle.data
        user.email = form.email.data
        user.role = form.role.data
        user.company = form.company.data
        user.city = form.city.data
        user.contacts = form.contacts.data
        db.session.add(user)
        db.session.commit()
        flash(u'Пользователь успешно создан')
        return redirect(url_for('.index'))
    context = dict()
    context['form'] = form
    context['app_version'] = app_version
    return render_template('accounts/profile.html', context=context)


@accounts.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edituser(user_id):
    """ Редактирование пользователя """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)

    form = AdminProfileForm(obj=user, edit=True)
    if form.validate_on_submit():
        user.name_first = form.name_first.data
        user.name_last = form.name_last.data
        user.name_middle = form.name_middle.data
        user.email = form.email.data
        user.role = form.role.data
        user.company = form.company.data
        user.city = form.city.data
        user.contacts = form.contacts.data
        db.session.add(user)
        db.session.commit()
        flash(u'Пользователь успешно изменен')
        return redirect(url_for('.index'))
    context = dict()
    context['form'] = form
    context['user'] = user
    context['app_version'] = app_version
    return render_template('accounts/profile.html', context=context)


@accounts.route('/deleteuser', methods=['POST'])
@login_required
@admin_required
def deleteuser():
    """ Удаление пользователя из базы"""
    User.query.filter_by(login=request.form.get('login')).delete()
    db.session.commit()
    flash(u'Пользователь успешно удален')
    return redirect(url_for('.index'))


@accounts.route('/deleteusers', methods=['POST'])
@login_required
@admin_required
def deleteusers():
    """ Удаление списка пользователей из базы """
    users = request.form.getlist('users[]')
    users = list(map(int, users))
    db.session.query(User).filter(User.id.in_(users)).delete(synchronize_session=False)
    db.session.commit()
    flash(u'Выбранные пользователи успешно удалены')
    return redirect(url_for('.index'))
