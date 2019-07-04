from api import *
from models.user import *
from models.recipe import *


@api.route('/recipe')
class RecipeRoute(Resource):
    # @api.doc(security='apikey')
    # @token_required
    # def get(self, current_user):
    def get(self):
        """ Get all recipes

        Returns a list containing all recipes in the database.
        """
        return RecipeSchema(many=True).dump(Recipe.query
                                            .options(joinedload('ingredients'))
                                            .options(joinedload('instructions'))
                                            .all()).data

    @api.doc(security='apikey')
    @api.expect(rest_recipe, validate=True)
    @token_required
    def post(self, current_user):
        # def post(self):
        """ Create a new recipe

        Stores a new recipe in the database.
        """
        data = api.payload
        recipe = Recipe(
            **{k: v for k, v in data.items()
               if k in {'dish', 'calories', 'description'}}
        )
        recipe.public_id = str(uuid.uuid4())
        db.session.add(recipe)

        for ingredient_data in data.get('ingredients'):
            ingredient = Ingredient(
                **{k: v for k, v in ingredient_data.items()
                   if k in {'product', 'quantity', 'unit'}}
            )
            ingredient.recipe = recipe
            db.session.add(ingredient)

        for instruction_data in data.get('instructions'):
            instruction = Instruction(
                **{k: v for k, v in instruction_data.items()
                   if k in {'instruction', 'step'}}
            )
            instruction.recipe = recipe
            db.session.add(instruction)

        db.session.commit()
        return data


@api.route('/recipe/<string:public_id>')
class SpecificRecipeRoute(Resource):
    # @api.doc(security='apikey')
    # @token_required
    # def get(self, current_user, public_id):
    def get(self, public_id):
        """ Get a specific recipe

        Return the specified recipe based on public_id
        """
        recipe = Recipe.query.options(joinedload('ingredients'))\
            .options(joinedload('instructions'))\
            .filter_by(public_id=public_id)\
            .first()

        if not recipe:
            return jsonify({'error': 'No recipe found'})

        return RecipeSchema().dump(recipe).data

    @api.doc(security='apikey')
    @token_required
    def delete(self, current_user, public_id):
        # def delete(self, public_id):
        """ Delete a specific recipe

        Deletes the specified recipe based on public_id
        """
        recipe = Recipe.query.options(joinedload('ingredients'))\
            .options(joinedload('instructions'))\
            .first()

        if not recipe:
            return jsonify({'error': 'No recipe found'})

        db.session.delete(recipe)
        db.session.commit()

        return jsonify({'message': 'Recipe has been deleted'})


@api.route('/recipe/<string:public_id>/favorite')
class FavoriteRecipeRoute(Resource):
    @api.doc(security='apikey')
    @token_required
    def put(self, current_user, public_id):
        """ Add a specific recipe to your favorites

        Adds the specified recipe based on public_id to the current users favorites
        """
        recipe = Recipe.query.options(joinedload('ingredients'))\
            .options(joinedload('instructions'))\
            .filter_by(public_id=public_id)\
            .first()

        if not recipe:
            return jsonify({'error': 'No recipe found'})

        token = request.headers['x-access-token']
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user = User.query.filter_by(public_id=data['public_id']).first()
        
        recipe.users.append(user)
        db.session.commit()
        
        return {'message': 'Added recipe to favorites'}, 200
