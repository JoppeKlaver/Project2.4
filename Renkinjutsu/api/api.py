from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restplus import Api, Resource, fields
from functools import wraps
from sqlalchemy.orm import joinedload, lazyload, load_only
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid
import datetime


app = Flask(__name__)

app.config.from_pyfile('config.py')

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'x-access-token'
    }
}


# Custom jwt decorater
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'error': 'No token!'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(
                public_id=data['public_id']).first()
        except:
            print(token)
            return jsonify({'error': 'Invalid token!'})

        return f(current_user, *args, **kwargs)

    return decorated


api = Api(app,
          authorizations=authorizations,
          version="1.0",
          title="Project 2.4 API",
          description="API for Project 2.4")

app.config['SWAGGER_UI_JSONEDITOR'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)


# Even tho PEP8 doesn't like it this is neccecary.
# Altho this looks like circular imports it's not actually that bad since
# I'm not actually using anything from views in api or vice versa. This is
# a limitation from the language apparently(?).
from views.login import *
from views.user import *
from views.user import *


if __name__ == '__main__':
    app.run(host='0.0.0.0')
