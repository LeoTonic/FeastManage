from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Roles:
    # Создание исполнителей, просмотр своих исполнителей
    # Добавление исполнителей на фестиваль
    USER = 1

    # Создание исполнителей, просмотр всех исполнителей
    # Добавление исполнителей на фестиваль
    # Создание фестиваля
    # Редактирование проживания
    # Редактирование питания
    # Редактирование транспорта
    MANAGER = 2

    # Создание исполнителей, просмотр всех исполнителей
    # Добавление исполнителей на фестиваль
    # Создание фестиваля
    # Редактирование проживания
    # Редактирование питания
    # Редактирование транспорта
    # Редактирование пользователей
    ADMIN = 3


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128), nullable=False)
    name_first = db.Column(db.String(128), nullable=False)
    name_last = db.Column(db.String(128))
    name_middle = db.Column(db.String(128))
    last_login_date = db.Column(db.DateTime, nullable=True)
    role = db.Column(db.Integer, default=Roles.USER)

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
            return u'Администратор'
        elif self.is_manager:
            return u'Менеджер'
        else:
            return u'Пользователь'

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
