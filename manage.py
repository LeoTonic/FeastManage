import os
from flask_migrate import MigrateCommand, Migrate
from flask_script import Shell, Manager, Server
from app import create_app, db
from app.models import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
manager = Manager(app)


def make_shell_context():
    return dict(db=db,
                User=User)


manager.add_command('runserver', Server(host='127.0.0.1', port=8192))
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


if __name__ == '__main__':
    manager.run()


