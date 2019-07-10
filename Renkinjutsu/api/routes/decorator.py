# from functools import wraps
# from flask import request, jsonify


# # Custom jwt decorater
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None

#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']

#         if not token:
#             # return jsonify({'error': 'No token!'})
#             return 'No token!', 404

#         try:
#             data = jwt.decode(token, app.config['SECRET_KEY'])
#             current_user = User.query.filter_by(
#                 public_id=data['public_id']).first()
#         except:
#             print(token)
#             return jsonify({'error': 'Invalid token!'})

#         return f(current_user, *args, **kwargs)

#     return decorated