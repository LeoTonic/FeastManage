from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from .views import page_not_found, server_error

app_version = '1.0.0'

bootstrap = Bootstrap()
db = SQLAlchemy(session_options={'autoflush': False})
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .performers.views import performers as performers_blueprint
    app.register_blueprint(performers_blueprint)

    # register error handlers
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_error)

    print('create app for {} configuration'.format(config_name))

    return app