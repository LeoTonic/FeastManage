from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app import app_version, db
from app.accounts import admin_required
from app.models import Category, Gentre

categories = Blueprint('categories', __name__)


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
    context['items'] = Category.query.all()
    return render_template('categories/index.html', context=context)
