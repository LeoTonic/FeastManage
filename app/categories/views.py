from flask import Blueprint, render_template, request
from flask_login import login_required
from app import app_version, db
from app.accounts import admin_required
from app.models import GentreGroup, Gentre

categories = Blueprint('categories', __name__)


@categories.route('/gengroups', methods=['GET', 'POST'])
@login_required
@admin_required
def gengroups():
    """Обработка списка групповых жанров"""
    if request.method == 'POST':
        # Запись нового группового жанра или обновление
        gengroup = GentreGroup.query.filter_by(id=request.form.get('id')).first()
        if gengroup is None:
            gengroup = GentreGroup()
        gengroup.title = request.form.get('title')
        db.session.add(gengroup)
        db.session.commit()
    context = dict()
    context['app_version'] = app_version
    context['title'] = u'Групповой жанр'
    context['listitems'] = GentreGroup.query.all()
    context['mode_gengroups'] = True
    return render_template('categories/index.html', context=context)


@categories.route('/gentres', defaults={'group_id': 0})
@categories.route('/gentres/<int:group_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def gentres(group_id):
    """Обработка жанров"""
    if request.method == 'POST':
        # Запись жанра или обновление
        print(request.form.get('id'))
        print(request.form.get('group_id'))
        print(request.form.get('title'))
    context = dict()
    context['app_version'] = app_version
    context['title'] = u'Жанр'
    context['rootselected'] = None
    rootitems = GentreGroup.query.all()
    if len(rootitems) > 0:
        context['rootitems'] = rootitems
        for item in rootitems:
            if item.id == group_id:
                context['rootselected'] = item
                break
        if context['rootselected'] is None:
            context['rootselected'] = rootitems[0]
            group_id = rootitems[0].id
    context['listitems'] = Gentre.query.filter_by(group_id=group_id).all()
    context['mode_gentres'] = True
    return render_template('categories/index.html', context=context)
