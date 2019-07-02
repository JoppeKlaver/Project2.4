from api import *
from models.user import *
from models.recipe import *


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


# Testing
# @app.route('/test', methods=['GET'])
# def test_get():
#     user = User.query.first()
#     user_schema = UserSchema()
#     output = user_schema.dump(user).data
#     return jsonify({'user': output})
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
    def get(self):
        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            return jsonify({'error': 'No user found'})

        return user


@api.route('/login')
class LoginRoute(Resource):
    @api.doc('user login')
    @api.expect(validate=True)
    def get(self):
        # post_data = request.json
        # return Auth.login_user(data=post_data)

        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return make_response('Unable to verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

        user = User.query.filter_by(username=auth.username).first()

        if not user:
            # return jsonify({'error' : 'User not found'})
            return make_response('Unable to verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

        if check_password_hash(user.password, auth.password):
            token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=42)}, app.config['SECRET_KEY'])

            return jsonify({'token': token.decode("UTF-8")})

        return make_response('Unable to verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@api.route('/recipe')
class RecipeRoute(Resource):
    def get(self):
        # recipe = Recipe.query.first()
        # recipe_schema = RecipeSchema()
        # output = recipe_schema.dump(recipe).data
        # return jsonify({'recipe': output})
        schema = RecipeSchema(many=True)
        return schema.dump(Recipe.query
                           .options(joinedload('ingredients'))
                           .all()).data


# CRUD Users
# @app.route('/user', methods=['GET'])
# @token_required
# def get_all_users(current_user):
#     if not create_user.admin:
#         return jsonify({'error': 'Admin rights required'})

#     users = User.query.all()

#     output = []

#     for user in users:
#         user_data = {}
#         user_data['public_id'] = user.public_id
#         user_data['admin'] = user.admin
#         user_data['username'] = user.username
#         user_data['password'] = user.password
#         output.append(user_data)

#     return jsonify({'users': output})


# @app.route('/user/<public_id>', methods=['GET'])
# @token_required
# def get_user(current_user, public_id):
#     user = User.query.filter_by(public_id=public_id).first()

#     if not user:
#         return jsonify({'error': 'No user found'})

#     user_data = {}
#     user_data['public_id'] = user.public_id
#     user_data['admin'] = user.admin
#     user_data['username'] = user.username
#     user_data['password'] = user.password

#     return jsonify({'user': user_data})


# @app.route('/user', methods=['POST'])
# @token_required
# def create_user(current_user):
#     if not current_user.admin:
#         return jsonify({'error': 'Admin rights required'})

#     data = request.get_json()

#     hash_password = generate_password_hash(data['password'], method='sha256')

#     new_user = User(public_id=str(uuid.uuid4()),
#                     username=data['username'], password=hash_password, admin=False)
#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({'message': 'New user created'})


# @app.route('/user/<public_id>', methods=['PUT'])
# @token_required
# def update_user(current_user, public_id):
#     if not current_user.admin:
#         return jsonify({'error': 'Admin rights required'})

#     # To-do: Update and refactor this function to input nececary changes.
#     user = User.query.filter_by(public_id=public_id).first()

#     if not user:
#         return jsonify({'error': 'No user found'})

#     user.admin = True
#     db.session.commit()

#     return jsonify({'message': 'User has been changed'})


# @app.route('/user/<public_id>', methods=['DELETE'])
# @token_required
# def delete_user(current_user, public_id):
#     if not current_user.admin:
#         return jsonify({'error': 'Admin rights required'})

#     user = User.query.filter_by(public_id=public_id).first()

#     if not user:
#         return jsonify({'error': 'No user found'})

#     db.session.delete(user)
#     db.session.commit()

#     return jsonify({'message': 'User has been deleted'})


# # Login
# @app.route('/login')
# def login():
#     auth = request.authorization

#     if not auth or not auth.username or not auth.password:
#         return make_response('Unable to verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

#     user = User.query.filter_by(username=auth.username).first()

#     if not user:
#         # return jsonify({'error' : 'User not found'})
#         return make_response('Unable to verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

#     if check_password_hash(user.password, auth.password):
#         token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow(
#         ) + datetime.timedelta(minutes=42)}, app.config['SECRET_KEY'])

#         return jsonify({'token': token.decode("UTF-8")})

#     return make_response('Unable to verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
