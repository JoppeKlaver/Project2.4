from api import *
from models.user import *


@api.route('/user')
class UserRoute(Resource):
    @api.doc(security='apikey')
    @token_required
    def get(self, current_user):
        schema = UserSchema(many=True)
        return schema.dump(User.query
                           .options(joinedload('details'))
                           .options(joinedload('address'))
                           .all()).data

    @api.expect(rest_user)
    def post(self):
        test = api.payload
        user = User(
            **{k: v for k, v in test.items()
               if k in {'admin', 'username', 'password'}}
        )
        user.public_id = str(uuid.uuid4())
        user.password = generate_password_hash(user.password, method='sha256')
        user_address = Address(
            **{k: v for k, v in test.get('address')[0].items()
               if k in {'streetname', 'house_number', 'house_number_addition',
                        'zip_code', 'city'}}
        )
        user_address.user = user
        user_details = Details(
            **{k: v for k, v in test.get('details')[0].items()
               if k in {'first_name', 'insertion', 'last_name',
                        'gender', 'date_of_birth', 'height',
                        'weight', 'target_weight', 'phone_number',
                        'e_mail_address'}}
        )
        user_details.user = user
        # print(user)
        # print(user_address)
        # print(user_details)
        db.session.add(user)
        db.session.add(user_address)
        db.session.add(user_details)
        db.session.commit()
        return test


@api.route('/user/<string:public_id>')
class SpecificUserRoute(Resource):
    @api.doc(security='apikey')
    @token_required
    def get(self, current_user, public_id):
        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            return jsonify({'error': 'No user found'})

        schema = UserSchema()
        return schema.dump(user).data

    @api.doc(security='apikey')
    @token_required
    def delete(self, current_user, public_id):
        # if not current_user.admin:
        #     return jsonify({'error': 'Admin rights required'})

        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            return jsonify({'error': 'No user found'})

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User has been deleted'})
