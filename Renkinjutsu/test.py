from flask import Flask
from flask_restplus import Api, Resource, fields as rest_fields
from flask_marshmallow import Marshmallow, Schema, fields

app = Flask(__name__)
api = Api(app)
ma = Marshmallow(app)


# Python
class Test(object):
    def __init__(self, character, number):
        self.character = character
        self.number = number

    def __repr__(self):
        return'character is {}, number is {}'.format(self.character, self.number)


# Marshmellow
class TestSchema(Schema):
    # character = fields.String()
    # number = fields.Integer()
    fields = ("character", "number")

    # @post_load
    # def create_test(self, data):
    #     return Test(**data)


# REST Plus
rest_test = api.model('Test', {'character': rest_fields.String('a character'), 'number': rest_fields.Integer('a number')})

tests = []
first = Test('a', 1)
tests.append(first)


@api.route('/test')
class Test(Resource):

    def get(self):
        schema = TestSchema(many=True)
        # return schema.dump(tests)
        return schema.jsonify(tests)

    @api.expect(rest_test)
    def post(self):
        tests.append(api.payload)
        return {'message': 'Message succesfully added'}, 201

# @api.route('/user')
# class Test(Resource):
#     def get(self):
#         return {'Message': 'Test succesfull'}


if __name__ == '__main__':
    app.run(debug=True)
