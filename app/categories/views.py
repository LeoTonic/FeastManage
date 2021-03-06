from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from flask_login import login_required
from app import app_version, db
from app.accounts import admin_required
from app.models import Category, Gentre, Age, Direction, Composition, Level

categories = Blueprint('categories', __name__)


class SubCategory:
    GENTRE = 'categories.gentres'
    AGE = 'categories.ages'
    DIRECTION = 'categories.directions'
    COMPOSITION = 'categories.compositions'
    LEVEL = 'categories.levels'


@categories.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    """Обработка категорий"""
    if request.method == 'POST':
        # Запись новой категории или обновление
        category = Category.query.filter_by(id=request.form.get('id')).first()
        if category is None:
            category = Category()
        category.title = request.form.get('title')
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('.index'))

    context = dict()
    context['app_version'] = app_version
    context['categories'] = Category.query.all()
    return render_template('categories/index.html', context=context)


@categories.route('/delete', methods=['POST'])
@login_required
@admin_required
def category_delete():
    """Удаление выбранной категории"""
    Category.query.filter_by(id=request.form.get('id')).delete()
    db.session.commit()
    flash(u'Категория успешно удалена')
    return redirect(url_for('.index'))


@categories.route('/<int:category_id>/gentres', methods=['GET', 'POST'])
@login_required
@admin_required
def gentres(category_id):
    """Обработка жанров"""
    if request.method == 'POST':
        # Запись нового жанра или обновление
        gentre = Gentre.query.filter_by(id=request.form.get('id')).first()
        if gentre is None:
            gentre = Gentre()
        gentre.title = request.form.get('title')
        gentre.category_id = category_id
        db.session.add(gentre)
        db.session.commit()
        return redirect(url_for('.gentres', category_id=category_id))

    context = dict()
    context['app_version'] = app_version
    context['mode_gentre'] = True
    context['mode_url'] = SubCategory.GENTRE
    context['categories'] = Category.query.all()
    context['category'] = category_id
    context['items'] = Gentre.query.filter_by(category_id=category_id).all()
    return render_template('categories/index.html', context=context)


@categories.route('/<int:category_id>/ages', methods=['GET', 'POST'])
@login_required
@admin_required
def ages(category_id):
    """Обработка возрастных групп"""
    if request.method == 'POST':
        # Запись новой группы или обновление
        age = Age.query.filter_by(id=request.form.get('id')).first()
        if age is None:
            age = Age()
        age.title = request.form.get('title')
        age.category_id = category_id
        db.session.add(age)
        db.session.commit()
        return redirect(url_for('.ages', category_id=category_id))
    context = dict()
    context['app_version'] = app_version
    context['mode_age'] = True
    context['mode_url'] = SubCategory.AGE
    context['categories'] = Category.query.all()
    context['category'] = category_id
    context['items'] = Age.query.filter_by(category_id=category_id).all()
    return render_template('categories/index.html', context=context)


@categories.route('/<int:category_id>/directions', methods=['GET', 'POST'])
@login_required
@admin_required
def directions(category_id):
    """Обработка направлений"""
    if request.method == 'POST':
        # Запись новой или обновление
        direction = Direction.query.filter_by(id=request.form.get('id')).first()
        if direction is None:
            direction = Direction()
        direction.title = request.form.get('title')
        direction.category_id = category_id
        db.session.add(direction)
        db.session.commit()
        return redirect(url_for('.directions', category_id=category_id))
    context = dict()
    context['app_version'] = app_version
    context['mode_direction'] = True
    context['mode_url'] = SubCategory.DIRECTION
    context['categories'] = Category.query.all()
    context['category'] = category_id
    context['items'] = Direction.query.filter_by(category_id=category_id).all()
    return render_template('categories/index.html', context=context)


@categories.route('/<int:category_id>/compositions', methods=['GET', 'POST'])
@login_required
@admin_required
def compositions(category_id):
    """Обработка составов"""
    if request.method == 'POST':
        # Запись новой или обновление
        composition = Composition.query.filter_by(id=request.form.get('id')).first()
        if composition is None:
            composition = Composition()
        composition.title = request.form.get('title')
        composition.category_id = category_id
        db.session.add(composition)
        db.session.commit()
        return redirect(url_for('.compositions', category_id=category_id))
    context = dict()
    context['app_version'] = app_version
    context['mode_composition'] = True
    context['mode_url'] = SubCategory.COMPOSITION
    context['categories'] = Category.query.all()
    context['category'] = category_id
    context['items'] = Composition.query.filter_by(category_id=category_id).all()
    return render_template('categories/index.html', context=context)


@categories.route('/<int:category_id>/levels', methods=['GET', 'POST'])
@login_required
@admin_required
def levels(category_id):
    """Обработка уровней"""
    if request.method == 'POST':
        # Запись новой или обновление
        level = Level.query.filter_by(id=request.form.get('id')).first()
        if level is None:
            level = Level()
        level.title = request.form.get('title')
        level.category_id = category_id
        db.session.add(level)
        db.session.commit()
        return redirect(url_for('.levels', category_id=category_id))
    context = dict()
    context['app_version'] = app_version
    context['mode_level'] = True
    context['mode_url'] = SubCategory.LEVEL
    context['categories'] = Category.query.all()
    context['category'] = category_id
    context['items'] = Level.query.filter_by(category_id=category_id).all()
    return render_template('categories/index.html', context=context)


@categories.route('/<int:category_id>/subdelete', methods=['POST'])
@login_required
@admin_required
def items_delete(category_id):
    """Удаление подкатегорий"""
    mode_url = request.form.get('mode_url')
    items = request.form.getlist('items[]')
    items = list(map(int, items))

    if mode_url == SubCategory.GENTRE:
        db.session.query(Gentre).filter(Gentre.id.in_(items)).delete(synchronize_session=False)
    elif mode_url == SubCategory.AGE:
        db.session.query(Age).filter(Age.id.in_(items)).delete(synchronize_session=False)
    elif mode_url == SubCategory.DIRECTION:
        db.session.query(Direction).filter(Direction.id.in_(items)).delete(synchronize_session=False)
    elif mode_url == SubCategory.COMPOSITION:
        db.session.query(Composition).filter(Composition.id.in_(items)).delete(synchronize_session=False)
    elif mode_url == SubCategory.LEVEL:
        db.session.query(Level).filter(Level.id.in_(items)).delete(synchronize_session=False)
    else:
        abort(404)
    db.session.commit()
    flash(u'Подкатегории успешно удалены')
    return redirect(url_for(mode_url, category_id=category_id))
