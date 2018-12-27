from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Roles:
    # Создание исполнителей, просмотр своих исполнителей
    # Добавление исполнителей на фестиваль
    USER = 1
    USER_NAME = u'Пользователь'

    # Создание исполнителей, просмотр всех исполнителей
    # Добавление исполнителей на фестиваль
    # Создание фестиваля
    # Редактирование проживания
    # Редактирование питания
    # Редактирование транспорта
    MANAGER = 2
    MANAGER_NAME = u'Менеджер'

    # Создание исполнителей, просмотр всех исполнителей
    # Добавление исполнителей на фестиваль
    # Создание фестиваля
    # Редактирование проживания
    # Редактирование питания
    # Редактирование транспорта
    # Редактирование пользователей
    ADMIN = 3
    ADMIN_NAME = u'Администратор'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # логин для авторизации
    login = db.Column(db.String(128), unique=True, nullable=False)
    # хэш пароля
    password_hash = db.Column(db.String(128))
    # электронная почта
    email = db.Column(db.String(128), nullable=False)
    # имя
    name_first = db.Column(db.String(128), nullable=False)
    # фамилия
    name_last = db.Column(db.String(128), nullable=False)
    # отчество
    name_middle = db.Column(db.String(128))
    # дата последней авторизации
    last_login_date = db.Column(db.DateTime, nullable=True)
    # роль пользователя в приложении
    role = db.Column(db.Integer, default=Roles.USER)
    # пользователь установил пароль при первом входе
    has_password = db.Column(db.Boolean, default=False)
    # организация
    company = db.Column(db.String(255))
    # населенный пункт
    city = db.Column(db.String(255))
    # контактные телефоны
    contacts = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def role_name(self):
        if self.is_administrator:
            return Roles.ADMIN_NAME
        elif self.is_manager:
            return Roles.MANAGER_NAME
        else:
            return Roles.USER_NAME

    @property
    def is_administrator(self):
        return self.role == Roles.ADMIN

    @property
    def is_manager(self):
        return self.role == Roles.MANAGER

    def __repr__(self):
        return '<User: {}>'.format(self.login)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
