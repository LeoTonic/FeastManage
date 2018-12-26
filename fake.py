from app import db
from app.models import User, Roles


def clear_database():
    User.query.delete()
    db.session.commit()
    print('data base cleared')


def create_superuser():
    a = User()
    a.login = 'admin'
    a.name_first = 'Администратор'
    a.email = 'admin@gmail.com'
    a.password = 'inferno'
    a.role = Roles.ADMIN
    db.session.add(a)
    db.session.commit()
    print('super user added')


def fake_users():
    counter = 0
    for x in range(10):
        u = User()
        u.login = 'user{}'.format(x)
        u.name_first = 'Пользователь {}'.format(x)
        u.email = 'user{}@gmail.com'.format(x)
        u.password = '123'
        u.role = Roles.USER
        db.session.add(u)
        counter += 1
        m = User()
        m.login = 'manager{}'.format(x)
        m.name_first = 'Менеджер {}'.format(x)
        m.email = 'manager{}@gmail.com'.format(x)
        m.password = '123'
        m.role = Roles.MANAGER
        db.session.add(m)
        counter += 1
        a = User()
        a.login = 'admin{}'.format(x)
        a.name_first = 'Администратор {}'.format(x)
        a.email = 'admin{}@gmail.com'.format(x)
        a.password = '123'
        a.role = Roles.ADMIN
        db.session.add(a)
        counter += 1
    db.session.commit()
    print('fake users added successfully: {}'.format(counter))
