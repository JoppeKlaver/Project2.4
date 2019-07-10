import logging
import traceback
import settings
import jwt

from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound
from flask_marshmallow import Marshmallow
from functools import wraps
from flask import request

from database.models import User

log = logging.getLogger(__name__)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'x-access-token'
    }
}

api = Api(version='1.0', title='Project 2.4 API', authorizations=authorizations,
          description='A Flask RestPlus powered API for Project 2.4')


ma = Marshmallow()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            # return jsonify({'error': 'No token!'})
            return {'error': 'No token!'}, 401

        try:
            data = jwt.decode(token, 'philosophersstone')
            current_user = User.query.filter_by(
                public_id=data['public_id']).first()
        except:
            return {'error': 'Invalid token!'}, 403

        return f(current_user, *args, **kwargs)

    return decorated


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404
