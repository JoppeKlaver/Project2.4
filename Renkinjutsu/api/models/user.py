from api import db, ma, api, fields


# SQL Alchemy
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)

    admin = db.Column(db.Boolean, default=False)

    username = db.Column(db.String(42), unique=True)
    password = db.Column(db.String(100))

    address = db.relationship('Address', backref='user')
    details = db.relationship('Details', backref='user', lazy="joined")

    def __repr__(self):
        return 'admin: {}, username: {}, password: {}'.format(self.admin, self.username, self.password)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    streetname = db.Column(db.String(100))
    house_number = db.Column(db.Integer)
    house_number_addition = db.Column(db.String(100))
    zip_code = db.Column(db.String(100))
    city = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'streetname: {}, house_number: {}, house_number_addition: {}, zip_code: {}, city: {}'.format(self.streetname, self.house_number, self.house_number_addition, self.zip_code, self.city)


class Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(100))
    insertion = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    gender = db.Column(db.String(10))
    date_of_birth = db.Column(db.DateTime)

    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    target_weight = db.Column(db.Integer)

    e_mail_address = db.Column(db.String(100))
    phone_number = db.Column(db.String(13))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'first_name: {}, insertion: {}, last_name: {}, gender: {}, date_of_birth: {}, height: {}, weight: {}, target_weight: {}, phone_number: {}, e_mail_address: {}'.format(self.first_name, self.insertion, self.last_name, self.gender, self.date_of_birth, self.height, self.weight, self.target_weight, self.phone_number, self.e_mail_address)


# Marshmallow
class AddressSchema(ma.ModelSchema):
    class Meta:
        model = Address


class DetailsSchema(ma.ModelSchema):
    class Meta:
        model = Details


class UserSchema(ma.ModelSchema):
    details = ma.Nested(DetailsSchema, many=True)
    address = ma.Nested(AddressSchema, many=True)

    class Meta:
        model = User


# RESTplus
# rest_user = api.model('User', {
#     "admin": fields.Boolean('Boolean to set admin rights'),
#     "address": {
#         "city": fields.String('City'),
#         "streetname": fields.String('Streetname'),
#         "zip_code": fields.String('Zip code'),
#         "house_number": fields.Integer('House number'),
#         "house_number_addition": fields.Integer('House number addition')
#     },
#     "username": fields.String('Username'),
#     "password": fields.String('Password'),
#     "details": {
#         "gender": fields.String('Gender'),
#         "insertion": fields.String('Insertion'),
#         "last_name": fields.String('Last name'),
#         "weight": fields.Integer('Current weight'),
#         "phone_number": fields.Integer('Phone number'),
#         "date_of_birth": fields.Date(),
#         "e_mail_address": fields.String('E-mail address'),
#         "first_name": fields.String('First name'),
#         "target_weight": fields.Integer('Target weight'),
#         "height": fields.Integer('Current lenght')
#     }
# })

# rest_user = api.model('User', {
#     "admin": fields.Boolean('Boolean to set admin rights'),
#     "username": fields.String('Username'),
#     "password": fields.String('Password'),
#     "phone_number": fields.Integer('Phone number'),
#     "e_mail_address": fields.String('E-mail address'),
#     "first_name": fields.String('First name'),
#     "insertion": fields.String('Insertion'),
#     "last_name": fields.String('Last name'),
#     "gender": fields.String('Gender'),
#     "date_of_birth": fields.Date(),
#     "height": fields.Integer('Current lenght'),
#     "weight": fields.Integer('Current weight'),
#     "target_weight": fields.Integer('Target weight'),
#     "streetname": fields.String('Streetname'),
#     "house_number": fields.Integer('House number'),
#     "house_number_addition": fields.Integer('House number addition'),
#     "zip_code": fields.String('Zip code'),
#     "city": fields.String('City'),
# })

# rest_user = api.model(
#     'User',
#     {
#         "admin": fields.Boolean('Boolean to set admin rights'),
#         "username": fields.String('Username'),
#         "password": fields.String('Password'),

#     })

rest_user_address = api.model(
    'Address',
    {
        "city": fields.String('City'),
        "streetname": fields.String('Streetname'),
        "zip_code": fields.String('Zip code'),
        "house_number": fields.Integer('House number'),
        "house_number_addition": fields.Integer('House number addition')
    })

rest_user_details = api.model(
    'Details',
    {
        "gender": fields.String('Gender'),
        "insertion": fields.String('Insertion'),
        "last_name": fields.String('Last name'),
        "weight": fields.Integer('Current weight'),
        "phone_number": fields.Integer('Phone number'),
        "date_of_birth": fields.Date(),
        "e_mail_address": fields.String('E-mail address'),
        "first_name": fields.String('First name'),
        "target_weight": fields.Integer('Target weight'),
        "height": fields.Integer('Current lenght')
    })

rest_user = api.model(
    'User',
    {
        "admin": fields.Boolean('Boolean to set admin rights'),
        "username": fields.String('Username'),
        "password": fields.String('Password'),
        "details": fields.List(fields.Nested(rest_user_details)),
        "address": fields.List(fields.Nested(rest_user_address))
    })
