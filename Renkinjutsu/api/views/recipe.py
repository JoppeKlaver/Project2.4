from api import *
from models.user import *
from models.recipe import *


@api.route('/recipe')
class RecipeRoute(Resource):
    def get(self):
        # recipe = Recipe.query.first()
        # recipe_schema = RecipeSchema()
        # output = recipe_schema.dump(recipe).data
        # return jsonify({'recipe': output})

        # schema = RecipeSchema(many=True)
        # return schema.dump(Recipe.query
        #                    .options(joinedload('ingredients'))
        #                    .all()).data

        schema = RecipeSchema(many=True)
        return schema.dump(Recipe.query
                           .options(joinedload('ingredients'))
                           .options(joinedload('instructions'))
                           .all()).data

    @api.expect(rest_recipe)
    def post(self):
        pass
