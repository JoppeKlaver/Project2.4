from api import *
from models.user import *
from models.recipe import *
# from datetime import datetime


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

        address = False
        try:
            user_address = Address(
                **{k: v for k, v in data.get('address').items()
                   if k in {'streetname', 'house_number',
                            'house_number_addition', 'zip_code', 'city'}}
            )
            user_address.user = user
            # db.session.add(user_address)
            address = True
        except:
            pass

        details = False
        try:
            user_details = Details(
                **{k: v for k, v in data.get('details').items()
                   if k in {'first_name', 'insertion', 'last_name',
                            'gender', 'date_of_birth', 'height',
                            'weight', 'target_weight', 'phone_number',
                            'e_mail_address'}}
            )
            year, month, day = user_details.date_of_birth.split('-')

            datetime.datetime(int(year), int(month), int(day))

            user_details.user = user
            # db.session.add(user_details)
            details = True
        except ValueError:
            return {'error': 'Date of birth is formatted wrong. Expected: \'YYYY-MM-DD\', received: \'{}\''.format(user_details.date_of_birth)}, 422
        except:
            pass

        if address:
            db.session.add(user_address)
        if details:
            db.session.add(user_details)
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

    @api.expect(rest_user_complete)
    def put(self, public_id):
        """ Update a specific user

        Update a specific user
        """
        # cb4ebb42-6c19-4288-8664-6685e0a1174f
        exclude = {'username', 'details', 'address'}
        user = UserSchema().dump(User.query.filter_by(public_id=public_id).first()).data
        # print(user)
        data = api.payload
        # put_user, put_address, put_details = False
        put = False
        for k, v in data.items():
            if k in user and k not in exclude:
                if k == 'password':
                    if not check_password_hash(user['password'], v):
                        user['password'] = generate_password_hash(v, method='sha256')
                        # print('password has been changed')
                        put = True
                        break
                if user.get(k) != v:
                    # print('{} becomes {}'.format(k, v))
                    user[k] = v
                    put = True
        if data['details']:
            try:
                year, month, day = data['details']['date_of_birth'].split('-')
                datetime.datetime(int(year), int(month), int(day))
            except ValueError:
                return {'error': 'Date of birth is formatted wrong. Expected: \'YYYY-MM-DD\', received: \'{}\''.format(data['details']['date_of_birth'])}, 422
            for k, v in data['details'].items():
                if k in user['details'] and user['details'][k] is not v:
                    print('{} becomes {}'.format(k, v))
                    user['details'][k] = v
                    put = True
        if data['address']:
            for k, v in data['address'].items():
                if k in user['address'] and user['address'][k] is not v:
                    print('{} becomes {}'.format(k, v))
                    user['address'][k] = v
                    put = True
        if put is True:
            print(user)
            db.session.query(User).filter_by(public_id=public_id).update(user)
            db.session.commit()



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
