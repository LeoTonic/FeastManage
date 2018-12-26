from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from app.models import Roles, User
from wtforms import ValidationError


class LoginForm(FlaskForm):
    """ Форма авторизации пользователя """
    login = StringField(u'Логин', validators=[DataRequired(), Length(1, 128)])
    password = PasswordField(u'Пароль', validators=[DataRequired()])
    remember_me = BooleanField(u'Запомнить пользователя')
    submit = SubmitField(u'Авторизация')


class PasswordForm(FlaskForm):
    """
    Форма установка пароля
    Впервые или для изменения
    """
    password = PasswordField(u'Пароль', validators=[
        DataRequired(), Length(min=6, max=128),
        EqualTo('confirm', message=u'Пароли должны совпадать')])
    confirm = PasswordField(u'Пароль повторно')
    submit = SubmitField(u'Сохранить')


class AdminProfileForm(FlaskForm):
    """
    Форма регистрации, редактирования пользователя
    """
    name_first = StringField(u'Имя', validators=[DataRequired(), Length(1, 128)])
    name_last = StringField(u'Фамилия')
    name_middle = StringField(u'Отчество')
    email = StringField(u'Электронная почта', validators=[DataRequired(), Length(1, 128), Email()])
    company = StringField(u'Организация', validators=[Length(max=128)])
    phone1 = StringField(u'Контактный телефон 1')
    phone2 = StringField(u'Контактный телефон 2')
    fax = StringField(u'Факс')
    login = StringField(u'Логин', validators=[DataRequired(), Length(1, 128)])
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
