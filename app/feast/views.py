from flask import Blueprint, render_template
from flask_login import login_required
from app import app_version
from app.accounts import notuser_required

feast = Blueprint('feast', __name__)


@feast.route('/', methods=['GET', 'POST'])
@login_required
@notuser_required
def index():
    context = dict()
    context['app_version'] = app_version
    return render_template('feast/index.html', context=context)
