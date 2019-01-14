import os
import random
from app import db
from app.models import User, Roles, Category, Gentre, Age, Direction, Composition, Level


def clear_database():
    User.query.delete()
    Gentre.query.delete()
    Age.query.delete()
    Direction.query.delete()
    Composition.query.delete()
    Level.query.delete()
    Category.query.delete()

    db.session.commit()
    print('data base cleared')


def create_superuser():
    a = User()
    a.login = 'admin'
    a.password = os.getenv('ADMIN_PASSWORD')
    a.name_first = 'Администратор'
    a.name_last = 'Администраторов'
    a.email = 'admin@gmail.com'
    a.role = Roles.ADMIN
    db.session.add(a)
    db.session.commit()
    print('super user added')


def fake_users():
    nl_arr = [
        'Иванов',
        'Петров',
        'Сидоров',
        'Михайлов',
        'Попов'
    ]
    nm_arr = [
        'Сергеевич',
        'Павлович',
        'Андреевич',
        'Тимофеевич',
        'Аркадьевич'
    ]
    nf_arr = [
        'Семен',
        'Анатолий',
        'Константин',
        'Василий',
        'Геннадий'
    ]
    c_arr = [
        'Москва',
        'Екатеринбург',
        'Сочи',
        'Владивосток',
        'Красноярск'
    ]

    cm_arr = [
        'ЗАО Ария',
        'ЗАО Комплект',
        'ПАО Территория',
        'ПАО Рассвет',
        'ЗАО Иволга'
    ]
    counter = 0
    for x in range(10):
        u = User()
        u.login = 'user{}'.format(x)
        u.name_first = random.choice(nf_arr)
        u.name_last = random.choice(nl_arr)
        u.name_middle = random.choice(nm_arr)
        u.email = 'example@example.com'
        u.city = random.choice(c_arr)
        u.company = random.choice(cm_arr)
        u.contacts = '(000) 123-45-67'
        u.role = Roles.USER
        db.session.add(u)
        counter += 1

    for x in range(10):
        u = User()
        u.login = 'manager{}'.format(x)
        u.name_first = random.choice(nf_arr)
        u.name_last = random.choice(nl_arr)
        u.name_middle = random.choice(nm_arr)
        u.email = 'example@example.com'
        u.city = random.choice(c_arr)
        u.company = random.choice(cm_arr)
        u.contacts = '(000) 123-45-67'
        u.role = Roles.MANAGER
        db.session.add(u)
        counter += 1

    u = User()
    u.login = 'admin0'
    u.name_first = random.choice(nf_arr)
    u.name_last = random.choice(nl_arr)
    u.name_middle = random.choice(nm_arr)
    u.email = 'example@example.com'
    u.city = random.choice(c_arr)
    u.company = random.choice(cm_arr)
    u.contacts = '(000) 123-45-67'
    u.role = Roles.ADMIN
    db.session.add(u)

    counter += 1
    db.session.commit()
    print('fake users added successfully: {}'.format(counter))


def create_categories():
    cat_counter = 0
    # Вокал
    cat = Category()
    cat.title = 'Вокал'
    db.session.add(cat)
    gen = Gentre()
    gen.title = 'Вокальное исполнительство'
    gen.category = cat
    db.session.add(gen)
    dir_array = [
        'Академическое',
        'Народное',
        'Детская песня',
        'Патриотическая песня'
    ]
    for item in dir_array:
        dir_new = Direction()
        dir_new.title = item
        dir_new.category = cat
        db.session.add(dir_new)
    com_array = [
        'Ансамбль',
        'Хор',
        'Соло',
        'Дуэт',
        'Трио',
        'Квартет'
    ]
    for item in com_array:
        com_new = Composition()
        com_new.title = item
        com_new.category = cat
        db.session.add(com_new)
    age_array = [
        'до 7 лет',
        '8-9 лет',
        '10-12 лет',
        '13-15 лет',
        '16-18 лет',
        '19-25 лет',
        '26-40 лет',
        'старше 40 лет',
        'смешанная'
    ]
    for item in age_array:
        age_new = Age()
        age_new.title = item
        age_new.category = cat
        db.session.add(age_new)
    lev_array = [
        'Начинающий',
        'Любительская',
        'Профессиональная',
    ]
    for item in lev_array:
        lev_new = Level()
        lev_new.title = item
        lev_new.category = cat
        db.session.add(lev_new)
    cat_counter += 1

    # Хореография
    cat = Category()
    cat.title = 'Хореография'
    db.session.add(cat)
    gen = Gentre()
    gen.title = 'Хореография'
    gen.category = cat
    db.session.add(gen)

    dir_array = [
        'Классический танец',
        'Народный танец',
        'Эстрадный танец',
        'Народно-сценический танец',
        'Стилизованный танец',
        'Бальная хореография',
        'Техники современного танца',
        'Мажоретки',
        'Театрально-хореографическая миниатюра',
        'Детский танец'
    ]
    for item in dir_array:
        dir_new = Direction()
        dir_new.title = item
        dir_new.category = cat
        db.session.add(dir_new)
    com_array = [
        'Ансамбль',
        'Ансамбль (мф)',
        'Соло',
    ]
    for item in com_array:
        com_new = Composition()
        com_new.title = item
        com_new.category = cat
        db.session.add(com_new)
    age_array = [
        'до 6 лет',
        '7-9 лет',
        '10-12 лет',
        '13-15 лет',
        '16-19 лет',
        '20-25 лет',
        'от 26 и старше',
        'смешанная'
    ]
    for item in age_array:
        age_new = Age()
        age_new.title = item
        age_new.category = cat
        db.session.add(age_new)
    lev_array = [
        'Начинающий',
        'Любительская',
        'Профессиональная',
        'Любители (особые)',
    ]
    for item in lev_array:
        lev_new = Level()
        lev_new.title = item
        lev_new.category = cat
        db.session.add(lev_new)
    cat_counter += 1

    db.session.commit()
    print('{} categories created'.format(cat_counter))
