import jwt
import logging
import datetime

from flask import request, jsonify
from flask_restplus import Resource
from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash, check_password_hash

from api import api, token_required
from database import db
from database.models import User, Recipe
from api.routes import create_recipe, update_recipe
from api.routes.serializers import RecipeSchema, IngredientSchema, IngredientSchema
from api.routes.serializers import rest_recipe, rest_ingredient, rest_instruction, put_recipe, put_ingredient, put_instruction

log = logging.getLogger(__name__)

ns = api.namespace(
    'favorite', description='Operations related to assigning favorite recipes')


@ns.response(401, 'No token')
@ns.response(403, 'Invalid token')
@ns.route('/favorite/<string:public_id>')
class RecipeArchiveCollection(Resource):
    @ns.doc(security='apikey')
    @ns.response(404, 'Recipe not found')
    @ns.response(201, 'Recipe successfully added to favorites')
    @token_required
    def post(self, current_user, public_id):
        """ Add a specific recipe to your favorites

        Adds the specified recipe based on public_id to the current users favorites
        """
        recipe = Recipe.query.options(joinedload('ingredients'))\
            .options(joinedload('instructions'))\
            .filter_by(public_id=public_id)\
            .first()

        if not recipe:
            return None, 404

        token = request.headers['x-access-token']
        data = jwt.decode(token, 'philosophersstone')
        user = User.query.filter_by(public_id=data['public_id']).first()

        recipe.users.append(user)
        db.session.commit()

        return None, 201

    @ns.doc(security='apikey')
    @ns.response(200, 'Success')
    @ns.response(404, 'No user found')
    @token_required
    def get(self, current_user, public_id):
        """ Get all favorite recipes of specified user

        Returns a list wirth all the favorite recipes for the specified recipe\
        based on public_id
        """
        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            return None, 404

        list = []
        for recipe in user.favorites:
            list.append(RecipeSchema().dump(recipe).data)

        return list, 200

    @ns.doc(security='apikey')
    @ns.response(404, 'No recipe found')
    @ns.response(204, 'Recipe successfully removed from favorites')
    @token_required
    def delete(self, current_user, public_id):
        """ Remove a specific recipe from your favorites

        Removes the specified recipe based on public_id from the current users favorites
        """
        recipe = Recipe.query.options(joinedload('ingredients'))\
            .options(joinedload('instructions'))\
            .filter_by(public_id=public_id)\
            .first()

        if not recipe:
            return None, 404

        token = request.headers['x-access-token']
        data = jwt.decode(token, 'philosophersstone')
        user = User.query.filter_by(public_id=data['public_id']).first()

        recipe.users.remove(user)
        db.session.commit()

        return None, 204
