from flask import Blueprint


bp = Blueprint('api', __name__, url_prefix='/api/v1')


@bp.route('/')
def hello_world():
    return 'You did it'
