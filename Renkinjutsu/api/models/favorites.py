from api import db, ma, api, fields

favorites = db.Table('favorites',
                     db.Column('user_id', db.Integer,
                               db.ForeignKey('user.id')),
                     db.Column('recipe_id', db.Integer,
                               db.ForeignKey('recipe.id')),
                     )
