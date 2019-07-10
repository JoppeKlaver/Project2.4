import logging

from flask import request
from flask_restplus import Resource
from sqlalchemy.orm import joinedload, lazyload, load_only

from api import api, token_required
from api.routes import create_user, rest_user_complete, update_user
from api.routes.serializers import UserSchema
from database.models import User

log = logging.getLogger(__name__)

ns = api.namespace('user', description='Operations related to users')


@ns.route('/')
class UserCollection(Resource):
    @api.doc(security='apikey')
    @ns.response(200, 'Success')
    @ns.response(401, 'No token')
    @ns.response(403, 'Invalid token')
    @token_required
    def get(self, current_user):
        """ Get all users

        Returns a list containing all users in the database.
        """
        schema = UserSchema(many=True)
        q = User.query\
            .options(lazyload('details'))\
            .options(joinedload('address'))\
            .all()
        return schema.dump(q)

    @api.response(400, 'Bad request')
    @api.response(201, 'User successfully created')
    @api.expect(rest_user_complete, validate=True)
    def post(self):
        """ Create a new user

        Stores a new user in the database.
        * Send a JSON object with the new user in the request body.
        ```
        {
            "admin": true,
            "username": "Admin",
            "password": "alpine12",
            "details": {
                "gender": "Male",
                "first_name": "Henk",
                "insertion": "van",
                "last_name": "Daar",
                "date_of_birth": "1989-01-01",
                "phone_number": "+31(0)691827364",
                "e_mail_address": "henk@daar.nl",
                "weight": 90,
                "target_weight": 80,
                "height": 172
            },
            "address": {
                "city": "Emmen",
                "streetname": "Ermerweg",
                "zip_code": "7812BG",
                "house_number": 68,
                "house_number_addition": "A"
            }
        }
        ```
        """
        create_user(self, api.payload)

        return None, 201


@ns.response(401, 'No token')
@ns.response(403, 'Invalid token')
@ns.response(404, 'User not found')
@ns.route('/<string:public_id>')
class UserItem(Resource):

    @ns.response(200, 'Success')
    @api.doc(security='apikey')
    @token_required
    def get(self, current_user, public_id):
        """ Get a specific user

        Return the specified user based on public_id

        """
        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            return None, 404

        schema = UserSchema()
        return schema.dump(user).data, 200

    @api.response(204, 'User deleted')
    @api.doc(security='apikey')
    @token_required
    def delete(self, current_user, public_id):
        """ Delete a specific user

        Deletes the specified user based on public_id
        """
        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            return None, 404

        db.session.delete(user)
        db.session.commit()

        return None, 204

    @api.response(400, 'Bad request')
    @api.response(204, 'User updated')
    @api.expect(rest_user_complete)
    @api.doc(security='apikey')
    @token_required
    def put(self, create_user, public_id):
        """ Update a specific user

        Use this method to update a specific user.

        * Send a JSON object with the new user in the request body.
        ```
        {
            "details": {
                "gender": "Gender",
                "first_name": "Name",
                "insertion": "Insertion",
                "last_name": "Surname",
                "date_of_birth": "1989-02-02",
                "phone_number": "+31(0)600000000",
                "e_mail_address": "new@email.com",
                "weight": 99,
                "target_weight": 99,
                "height": 199
            },
            "address": {
                "city": "City",
                "streetname": "Streetname",
                "zip_code": "Zip code",
                "house_number": 99,
                "house_number_addition": "Z"
            }
        }
        ```
        * Specify the public ID of the user to modify in the request URL path.
        """
        # cb4ebb42-6c19-4288-8664-6685e0a1174f
        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            return None, 404

        update_user(self, public_id)

        return None, 204
