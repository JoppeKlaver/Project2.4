from api import *
from models.user import *


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
