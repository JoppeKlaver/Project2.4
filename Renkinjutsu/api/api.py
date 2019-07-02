from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restplus import Api, Resource, fields
from functools import wraps
from sqlalchemy.orm import joinedload
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

api = Api(app,
          authorizations=authorizations,
          version="1.0",
          title="Project 2.4 API",
          description="API for Project 2.4")

db = SQLAlchemy(app)
ma = Marshmallow(app)


# Even tho PEP8 doesn't like it this is neccecary.
# Altho this looks like circular imports it's not actually that bad since
# I'm not actually using anything from views in api or vice versa. This is
# a limitation from the language apparently(?).
from views import *


if __name__ == '__main__':
    app.run()
