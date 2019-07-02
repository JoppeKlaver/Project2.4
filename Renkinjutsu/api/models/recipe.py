from api import db, ma


# SQL Alchemy
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)

    dish = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    calories = db.Column(db.Integer)

    ingredients = db.relationship('Ingredient', backref='recipe')


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    product = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    unit = db.Column(db.String(100))

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))


# Marshmallow
class IngredientSchema(ma.ModelSchema):
    class Meta:
        model = Ingredient


class RecipeSchema(ma.ModelSchema):
    ingredients = ma.Nested(IngredientSchema, many=True)

    class Meta:
        model = Recipe
