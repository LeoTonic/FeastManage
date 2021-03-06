from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jsglue import JSGlue
from config import config
from .views import page_not_found, server_error, method_not_allowed

app_version = '0.1.25'

bootstrap = Bootstrap()
db = SQLAlchemy(session_options={'autoflush': False})
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'accounts.login'
jsglue = JSGlue()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    jsglue.init_app(app)

    if not app.config['DEBUG'] and app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from .performers.views import performers as performers_blueprint
    app.register_blueprint(performers_blueprint)

    from .feast.views import feast as feast_blueprint
    app.register_blueprint(feast_blueprint, url_prefix='/feast')

    from .accounts.views import accounts as accounts_blueprint
    app.register_blueprint(accounts_blueprint, url_prefix='/accounts')

    from .categories.views import categories as categories_blueprint
    app.register_blueprint(categories_blueprint, url_prefix='/categories')

    # register error handlers
    app.register_error_handler(403, method_not_allowed)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_error)

    print('create app for {} configuration'.format(config_name))

    return app
