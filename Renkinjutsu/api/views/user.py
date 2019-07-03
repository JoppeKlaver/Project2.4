from api import *
from models.user import *
from models.recipe import *


@api.route('/user')
class UserRoute(Resource):
    @api.doc(security='apikey')
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

    @api.expect(rest_user_complete, validate=True)
    def post(self):
        """ Create a new user

        Stores a new user in the database.
        """
        data = api.payload

        user = User(
            **{k: v for k, v in data.items()
               if k in {'admin', 'username', 'password'}}
        )
        user.public_id = str(uuid.uuid4())
        user.password = generate_password_hash(user.password, method='sha256')

        try:
            user_address = Address(
                **{k: v for k, v in data.get('address').items()
                   if k in {'streetname', 'house_number',
                            'house_number_addition', 'zip_code', 'city'}}
            )
            user_address.user = user
            db.session.add(user_address)
        except:
            pass

        try:
            user_details = Details(
                **{k: v for k, v in data.get('details').items()
                   if k in {'first_name', 'insertion', 'last_name',
                            'gender', 'date_of_birth', 'height',
                            'weight', 'target_weight', 'phone_number',
                            'e_mail_address'}}
            )
            user_details.user = user
            db.session.add(user_details)
        except:
            pass

        db.session.add(user)
        db.session.commit()
        return data


@api.route('/user/<string:public_id>')
class SpecificUserRoute(Resource):
    @api.doc(security='apikey')
    @token_required
    def get(self, current_user, public_id):
        """ Get a specific recipe

        Return the specified recipe based on public_id
        """
        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            return jsonify({'error': 'No user found'})

        schema = UserSchema()
        return schema.dump(user).data

    @api.doc(security='apikey')
    @token_required
    def delete(self, current_user, public_id):
        """ Delete a specific user

        Deletes the specified user based on public_id
        """
        # if not current_user.admin:
        #     return jsonify({'error': 'Admin rights required'})

        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            return jsonify({'error': 'No user found'})

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User has been deleted'})


@api.route('/user/<string:public_id>/favorite')
class FavoriteUserRoute(Resource):
    @api.doc(security='apikey')
    @token_required
    def get(self, current_user, public_id):
        """ Get all favorite recipes of specified user

        Returns a list wirth all the favorite recipes for the specified recipe\
        based on public_id
        """
        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            return jsonify({'error': 'No user found'})

        list = []
        for recipe in user.favorites:
            list.append(RecipeSchema().dump(recipe).data)

        return list, 200
