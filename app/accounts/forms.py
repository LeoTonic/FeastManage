from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp
from app.models import Roles, User
from wtforms import ValidationError


class LoginForm(FlaskForm):
    """ Форма авторизации пользователя """
    login = StringField(u'Логин', validators=[
        DataRequired(u'Обязательное поле'),
        Length(1, 128)])
    password = PasswordField(u'Пароль', validators=[DataRequired(u'Обязательное поле')])
    remember_me = BooleanField(u'Запомнить пользователя')
    submit = SubmitField(u'Авторизация')


class PasswordForm(FlaskForm):
    """
    Форма установка пароля
    Впервые или для изменения
    """
    password = PasswordField(u'Пароль', validators=[
        DataRequired(u'Обязательное поле'),
        Length(min=6, max=128, message=u'Длина пароля должна составлять не менее 6 символов'),
        EqualTo('confirm', message=u'Пароли должны совпадать')])
    confirm = PasswordField(u'Пароль повторно')
    submit = SubmitField(u'Сохранить')


class AdminProfileForm(FlaskForm):
    """
    Форма регистрации, редактирования пользователя
    """
    name_first = StringField(u'Имя', validators=[DataRequired(u'Обязательное поле'), Length(1, 128)])
    name_last = StringField(u'Фамилия')
    name_middle = StringField(u'Отчество')
    email = StringField(u'Электронная почта', validators=[DataRequired(u'Обязательное поле'), Length(1, 128), Email()])
    company = StringField(u'Организация', validators=[Length(max=128)])
    phone1 = StringField(u'Телефон 1 (xxx) xxx-xx-xx')
    phone2 = StringField(u'Телефон 2 (xxx) xxx-xx-xx')
    fax = StringField(u'Факс (xxx) xxx-xx-xx')
    login = StringField(u'Логин', validators=[
        DataRequired(u'Обязательное поле'),
        Length(1, 128),
        Regexp('^[A-Za-z0-9_]+$',
               message=u'Логин может содержать только латинские буквы в любом регистре, цифры и знаки - . _')])
    role = SelectField(u'Роль', coerce=int)

    def __init__(self, user, *args, **kwargs):
        super(AdminProfileForm, self).__init__(*args, **kwargs)
        self.role.choices = [
            (Roles.USER, Roles.USER_NAME),
            (Roles.MANAGER, Roles.MANAGER_NAME),
            (Roles.ADMIN, Roles.ADMIN_NAME)
        ]
        self.user = user

    def validate_login(self, field):
        if self.user is not None:
            # Проверяем логин в форме редактирования
            if field.data != self.user.login and User.query.filter_by(login=field.data).first():
                raise ValidationError(u'Логин пользователя уже занят')
        else:
            # Проверяем логин в форме создания пользователя
            if User.query.filter_by(login=field.data).first():
                raise ValidationError(u'Логин пользователя уже занят')
