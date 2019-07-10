import datetime
import logging

import jwt
from flask import request
from flask_restplus import Resource
from sqlalchemy.orm import joinedload
from werkzeug.security import check_password_hash, generate_password_hash

from api import api, token_required
from api.routes import create_recipe, update_recipe
from api.routes.serializers import (IngredientSchema, RecipeSchema,
                                    put_ingredient, put_instruction,
                                    put_recipe, rest_ingredient,
                                    rest_instruction, rest_recipe)
from database import db
from database.models import Recipe

log = logging.getLogger(__name__)

ns = api.namespace('recipe', description='Operations related to recipes')


@ns.route('/')
class RecipeCollection(Resource):

    @ns.response(200, 'Success')
    def get(self):
        """ Get all recipes

        Returns a list containing all recipes in the database.
        """
        return RecipeSchema(many=True).dump(Recipe.query
                                            .options(joinedload('ingredients'))
                                            .options(joinedload('instructions'))
                                            .all()).data, 200

    @ns.doc(security='apikey')
    @ns.expect(rest_recipe, validate=True)
    @ns.response(401, 'No token')
    @ns.response(403, 'Invalid token')
    @ns.response(201, 'Recipe successfully created')
    @token_required
    def post(self, current_user):
        """ Create a new recipe

        Use this method to store a new recipe in the database.

        * Send a JSON object with the new recipe in the request body.
        ```
        {
            "dish": "Name",
            "description": "Description",
            "calories": 1000,
            "ingredients": [
                {
                "product": "Product 1",
                "quantity": 1,
                "unit": "Liter"
                },
                {
                "product": "Product 2",
                "quantity": 500,
                "unit": "Gram"
                }
            ],
            "instructions": [
                {
                "step": 1,
                "instruction": "Instruction 1"
                },
                {
                "step": 2,
                "instruction": "Instruction 2"
                }
            ]
        }
        ```
        """
        create_recipe(self, api.payload)

        return None, 201


@ns.response(404, 'Recipe not found.')
@ns.route('/<string:public_id>')
class RecipeItem(Resource):

    @ns.response(200, 'Success')
    def get(self, public_id):
        """ Get a specific recipe

        Return the specified recipe based on public_id
        """
        recipe = Recipe.query.options(joinedload('ingredients'))\
            .options(joinedload('instructions'))\
            .filter_by(public_id=public_id)\
            .first()

        if not recipe:
            return None, 404

        return RecipeSchema().dump(recipe).data, 200

    @ns.doc(security='apikey')
    @ns.response(401, 'No token')
    @ns.response(403, 'Invalid token')
    @ns.response(204, 'Recipe successfully deleted')
    @token_required
    def delete(self, current_user, public_id):
        """ Delete a specific recipe

        Deletes the specified recipe based on public_id
        """
        recipe = Recipe.query.options(joinedload('ingredients'))\
            .options(joinedload('instructions'))\
            .first()

        if not recipe:
            return None, 404

        db.session.delete(recipe)
        db.session.commit()

        return None, 204

    @ns.doc(security='apikey')
    @ns.expect(put_recipe)
    @ns.response(401, 'No token')
    @ns.response(403, 'Invalid token')
    @ns.response(204, 'Recipe successfully updated.')
    @token_required
    def put(self, current_user, public_id):
        """ Update a recipe

        Use this method to update a recipe

        * Send a JSON object with the updated recipe in the request body.
        ```
        {
            "dish": "Name",
            "description": "Description",
            "calories": 1000,
            "ingredients": [
                {
                "product": "Product 1",
                "quantity": 1,
                "unit": "Liter"
                },
                {
                "product": "Product 2",
                "quantity": 500,
                "unit": "Gram"
                }
            ],
            "instructions": [
                {
                "step": 1,
                "instruction": "Instruction 1"
                },
                {
                "step": 2,
                "instruction": "Instruction 2"
                }
            ]
        }
        ```
        * Specify the public ID of the recipe to modify in the request URL path.
        """
        # fc970b58-47d5-4fa5-b168-5de34dec3b49
        update_recipe(self, public_id, api.payload)

        return None, 204
