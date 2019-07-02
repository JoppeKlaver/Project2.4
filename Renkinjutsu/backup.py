from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps


app = Flask(__name__)


# JWT config
app.config['SECRET_KEY'] = 'philosophersstone'
# SQLAlchemy config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:alpine12''@localhost/alchemy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ORM
# User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Hersenspinsel; insead of using the id to reference users I'll try to generate
    #                a public_id with uid.
    # To-do: implement uid or something.
    public_id = db.Column(db.String(50), unique=True)
    admin = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(42), unique=True)
    password = db.Column(db.String(100))

    # def __init__(self, admin, username, password):
    #     self.admin = admin
    #     self.username = username
    #     self.password = password


# Test table
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# API
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
            create_user = User.query.filter_by(
                public_id=data['public_id']).first()
        except:
            return jsonify({'error': 'Invalid token!'})

        return f(create_user, *args, **kwargs)

    return decorated


# CRUD Users
@app.route('/user', methods=['GET'])
@token_required
def get_all_users(create_user):
    if not create_user.admin:
        return jsonify({'error': 'Admin rights required'})

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['admin'] = user.admin
        user_data['username'] = user.username
        user_data['password'] = user.password
        output.append(user_data)

    return jsonify({'users': output})


@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'error': 'No user found'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['admin'] = user.admin
    user_data['username'] = user.username
    user_data['password'] = user.password

    return jsonify({'user': user_data})


@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):
    if not current_user.admin:
        return jsonify({'error': 'Admin rights required'})

    data = request.get_json()

    hash_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()),
                    username=data['username'], password=hash_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created'})


@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def update_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'error': 'Admin rights required'})

    # To-do: Update and refactor this function to input nececary changes.
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'error': 'No user found'})

    user.admin = True
    db.session.commit()

    return jsonify({'message': 'User has been changed'})


@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'error': 'Admin rights required'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'error': 'No user found'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User has been deleted'})


# CRUD Test
@app.route('/test', methods=['GET'])
@token_required
def get_all_tests(current_user):
    tests = Test.query.filter_by(user_id=current_user.id).all()

    output = []

    for test in tests:
        test_data = {}
        test_data['id'] = test.id
        test_data['text'] = test.text
        test_data['complete'] = test.complete
        output.append(test_data)

    return jsonify({'tests': output})


@app.route('/test/<test_id>', methods=['GET'])
@token_required
def get_test(current_user, test_id):
    test = Test.query.filter_by(id=test_id, user_id=current_user.public_id).first()

    if not test:
        return jsonify({'error': 'Test not found!'})

    test_data = {}
    test_data['id'] = test.id
    test_data['text'] = test.text
    test_data['complete'] = test.complete

    return jsonify(test_data)


@app.route('/test', methods=['POST'])
@token_required
def create_test(current_user):
    data = request.get_json()

    new_test = Test(text=data['text'], complete=False, user_id=current_user.id)
    db.session.add(new_test)
    db.session.commit()

    return jsonify({'message': "test created!"})


@app.route('/test/<test_id>', methods=['PUT'])
@token_required
def complete_test(current_user, test_id):
    test = Test.query.filter_by(id=test_id, user_id=current_user.id).first()

    if not test:
        return jsonify({'message': 'No test found!'})

    test.complete = True
    db.session.commit()

    return jsonify({'message': 'test item has been completed!'})


@app.route('/test/<test_id>', methods=['DELETE'])
@token_required
def delete_test(current_user, test_id):
    test = Test.query.filter_by(id=test_id, user_id=current_user.id).first()

    if not test:
        return jsonify({'message': 'No test found!'})

    db.session.delete(test)
    db.session.commit()

    return jsonify({'message': 'test item deleted!'})


# Login
@app.route('/login')
def login():
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


# Debug
if __name__ == "__main__":
    app.run(debug=True)
