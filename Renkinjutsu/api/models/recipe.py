from api import db, ma, api, fields


# SQL Alchemy
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


# Marshmallow
class IngredientSchema(ma.ModelSchema):
    class Meta:
        model = Ingredient


class InstructionSchema(ma.ModelSchema):
    class Meta:
        model = Instruction


class RecipeSchema(ma.ModelSchema):
    ingredients = ma.Nested(IngredientSchema, many=True)
    instructions = ma.Nested(InstructionSchema, many=True)

    class Meta:
        model = Recipe


# RESTplus
rest_ingredient = api.model(
    'Ingredient',
    {
        "product": fields.String('The product to use'),
        "quantity": fields.Integer('Amount of said product'),
        "unit": fields.String('The unit in which the quantity field is quantified')
    })

rest_instruction = api.model(
    'Instruction',
    {
        "step": fields.Integer('Counter to order steps'),
        "instruction": fields.String('The instruction')
    })

rest_recipe = api.model(
    'Recipe',
    {
        "dish": fields.String('Name of the dish'),
        "description": fields.String('Description of the dish'),
        "calories": fields.Integer('Amount of calories in the dish'),
        "ingredients": fields.List(fields.Nested(rest_ingredient)),
        "instructions": fields.List(fields.Nested(rest_instruction))
    })
