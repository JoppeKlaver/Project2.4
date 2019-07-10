import jwt
import logging
import datetime

from flask import request, jsonify
from flask_restplus import Resource
from werkzeug.security import generate_password_hash, check_password_hash

from api import api, token_required
from database.models import User

log = logging.getLogger(__name__)

ns = api.namespace('login', description='Operations related to authentication')


@ns.route('/')
class LoginRoute(Resource):
    @ns.doc('user login')
    @ns.expect(validate=True)
    @ns.response(200, 'Login successfull')
    @ns.response(400, 'Form incomplete')
    @ns.response(401, 'No user found')
    @ns.response(403, 'Invalid credentials')
    def post(self):
        """ User login

        Authorization by JSON Web Token. Expects username and password and \
            returns a token.
        """
        # post_data = request.json
        # return Auth.login_user(data=post_data)
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return None, 400

        user = User.query.filter_by(username=auth.username).first()

        if not user:
            return None, 401

        if check_password_hash(user.password, auth.password):
            token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=42)}, 'philosophersstone')

            return {'token': token.decode("UTF-8")}, 200

        return None, 403
