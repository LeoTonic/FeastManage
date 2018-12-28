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
    a.name_last = 'Администраторов'
    a.email = 'admin@gmail.com'
    a.role = Roles.ADMIN
    db.session.add(a)
    db.session.commit()
    print('super user added')


def fake_users():
    counter = 0
    for x in range(15):
        u = User()
        u.login = 'user{}'.format(x)
        u.name_first = 'Имя {}'.format(x)
        u.name_last = 'Фамилия {}'.format(x)
        u.email = 'user{}@gmail.com'.format(x)
        u.city = 'Город {}'.format(x)
        u.company = 'Компания {}'.format(x)
        u.contacts = '(123) 123-12-12'
        u.role = Roles.USER
        db.session.add(u)
        counter += 1
    for x in range(15):
        u = User()
        u.login = 'manager{}'.format(x)
        u.name_first = 'МанИмя {}'.format(x)
        u.name_last = 'МанФам {}'.format(x)
        u.email = 'manager{}@gmail.com'.format(x)
        u.city = 'МанГород {}'.format(x)
        u.company = 'МанКомпания {}'.format(x)
        u.contacts = '(456) 123-12-12'
        u.role = Roles.MANAGER
        db.session.add(u)
        counter += 1

    db.session.commit()
    print('fake users added successfully: {}'.format(counter))
