from database import db


favorites = db.Table('favorites',
                     db.Column('user_id', db.Integer,
                               db.ForeignKey('user.id')),
                     db.Column('recipe_id', db.Integer,
                               db.ForeignKey('recipe.id')),
                     )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)

    admin = db.Column(db.Boolean, default=False)

    username = db.Column(db.String(42), unique=True)
    password = db.Column(db.String(100))

    address = db.relationship('Address', backref='user', uselist=False)
    details = db.relationship('Details', backref='user', uselist=False)

    favorites = db.relationship(
        'Recipe', secondary=favorites, backref=db.backref('users',
                                                          lazy='dynamic'))

    def __repr__(self):
        return '<User %r>' % self.username


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    streetname = db.Column(db.String(100))
    house_number = db.Column(db.Integer)
    house_number_addition = db.Column(db.String(100))
    zip_code = db.Column(db.String(100))
    city = db.Column(db.String(100))

    user_id = db.Column(db.ForeignKey('user.id'))
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'streetname: {}, house_number: {}, house_number_addition: {},\
            zip_code: {}, city: {}'.format(self.streetname, self.house_number,
                                           self.house_number_addition,
                                           self.zip_code, self.city)


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
        return '<Details %r>' % self.first_name


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)

    dish = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    calories = db.Column(db.Integer)

    ingredients = db.relationship('Ingredient', backref='recipe')
    instructions = db.relationship('Instruction', backref='recipe')


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    product = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    unit = db.Column(db.String(100))

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))


class Instruction(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    step = db.Column(db.Integer)
    instruction = db.Column(db.String(255))

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
