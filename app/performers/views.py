from flask import Blueprint

performers = Blueprint('performers', __name__)


@performers.route('/', methods=['GET', 'POST'])
def index():
    return 'Hello, World'
