from flask_restplus import fields

from api.renkinjutsu import api, ma
from database.models import User, Details, Address, Recipe, Ingredient, Instruction


# Marshmallow
class AddressSchema(ma.ModelSchema):
    class Meta:
        model = Address


class DetailsSchema(ma.ModelSchema):
    class Meta:
        model = Details


class UserSchema(ma.ModelSchema):
    details = ma.Nested(DetailsSchema, many=False, lazy='joined')
    address = ma.Nested(AddressSchema, many=False, lazy='joined')

    class Meta:
        model = User


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
rest_address = api.model(
    'Address',
    {
        "city": fields.String(example='City', required=True),
        "streetname": fields.String(example='Streetname', required=True),
        "zip_code": fields.String(example='0000AA', required=True),
        "house_number": fields.Integer(example=42, required=True),
        "house_number_addition": fields.String(example='B', required=False)
    })

rest_details = api.model(
    'Details',
    {
        "gender": fields.String(example='Other', required=True),
        "first_name": fields.String(example='Sjoerd', required=True),
        "insertion": fields.String(example='de', required=False),
        "last_name": fields.String(example='Boer', required=True),
        "date_of_birth": fields.Date(example='1900-01-01', required=True),
        "phone_number": fields.String(example='+31(0)691827364', required=True),
        "e_mail_address": fields.String(example='example@email.com', required=True),
        "weight": fields.Integer(example=75, required=True),
        "target_weight": fields.Integer(example=70, required=True),
        "height": fields.Integer(example=175, required=True)
    })

rest_user = api.model(
    'User',
    {
        "admin": fields.Boolean(required=True, example=False),
        "username": fields.String(required=True, example='Username'),
        "password": fields.String(required=True, example='p@ssw0rd!')
    })


rest_user_complete = api.inherit(
    'User Complete', rest_user,
    {
        "details": fields.Nested(rest_details, required=False),
        "address": fields.Nested(rest_address, required=False)
    })

rest_ingredient = api.model(
    'Ingredient',
    {
        "product": fields.String('The product to use'),
        "quantity": fields.Integer('Amount of said product', required=False),
        "unit": fields.String('The unit in which the quantity field is \
            quantified', required=False)
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

put_ingredient = api.model(
    'Ingredient',
    {
        "id": fields.Integer(example=1),
        "product": fields.String(example='Water'),
        "quantity": fields.Integer(example=1, required=False),
        "unit": fields.String(example='Liter', required=False)
    })

put_instruction = api.model(
    'Instruction',
    {
        "id": fields.Integer(example=1),
        "step": fields.Integer(example=1),
        "instruction": fields.String(example='Do something')
    })

put_recipe = api.model(
    'Recipe',
    {
        "dish": fields.String(example='Dish'),
        "description": fields.String(example='Description of the dish'),
        "calories": fields.Integer(example=666),
        "ingredients": fields.List(fields.Nested(put_ingredient)),
        "instructions": fields.List(fields.Nested(put_instruction))
    })