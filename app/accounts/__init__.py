"""
Модуль работы с учетными записями пользователей приложения
Авторизация, регистрация-редактирование, выход
"""
from flask import abort
from flask_login import current_user
from functools import wraps


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not current_user.is_administrator:
            abort(403)
        return f(*args, **kwargs)
    return wrap
