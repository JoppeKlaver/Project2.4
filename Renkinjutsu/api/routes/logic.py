from api import api
from database import db
from database.models import User, Details, Address, Recipe, Ingredient, Instruction
from werkzeug.security import generate_password_hash, check_password_hash
from .serializers import UserSchema, RecipeSchema

import uuid


def create_user(self, data):
    data = api.payload

    user = User(
        **{k: v for k, v in data.items()
           if k in {'admin', 'username', 'password'}}
    )
    user.public_id = str(uuid.uuid4())
    user.password = generate_password_hash(user.password, method='sha256')

    address = False
    try:
        user_address = Address(
            **{k: v for k, v in data.get('address').items()
               if k in {'streetname', 'house_number',
                        'house_number_addition', 'zip_code', 'city'}}
        )
        user_address.user = user
        # db.session.add(user_address)
        address = True
    except:
        pass

    details = False
    try:
        user_details = Details(
            **{k: v for k, v in data.get('details').items()
               if k in {'first_name', 'insertion', 'last_name',
                        'gender', 'date_of_birth', 'height',
                        'weight', 'target_weight', 'phone_number',
                        'e_mail_address'}}
        )
        year, month, day = user_details.date_of_birth.split('-')

        datetime.datetime(int(year), int(month), int(day))

        user_details.user = user
        # db.session.add(user_details)
        details = True
    except ValueError:
        return {'error': 'Date of birth is formatted wrong. Expected: \'YYYY-MM-DD\', received: \'{}\''.format(user_details.date_of_birth)}, 422
    except:
        pass

    if address:
        db.session.add(user_address)
    if details:
        db.session.add(user_details)
    db.session.add(user)
    db.session.commit()


def update_user(self, public_id):
    exclude = {'username', 'details', 'address'}
    u = User.query.filter_by(public_id=public_id).first()
    user = UserSchema().dump(u).data
    # print(user)
    data = api.payload
    put_user = False
    put_address = False
    put_details = False
    for k, v in data.items():
        if k in user and k not in exclude:
            if k == 'password':
                if not check_password_hash(user['password'], v):
                    user['password'] = generate_password_hash(
                        v, method='sha256')
                    # print('password has been changed')
                    put_user = True
                    break
            if user.get(k) != v:
                # print('{} becomes {}'.format(k, v))
                user[k] = v
                put_user = True
    try:
        if data['details']:
            try:
                year, month, day = data['details']['date_of_birth'].split(
                    '-')
                datetime.datetime(int(year), int(month), int(day))
            except ValueError:
                return {'error': 'Date of birth is formatted wrong. Expected: \'YYYY-MM-DD\', received: \'{}\''.format(data['details']['date_of_birth'])}, 422
            for k, v in data['details'].items():
                if k in user['details'] and user['details'][k] is not v:
                    print('{} becomes {}'.format(k, v))
                    user['details'][k] = v
                    put_details = True
    except:
        pass

    try:
        if data['address']:
            for k, v in data['address'].items():
                if k in user['address'] and user['address'][k] is not v:
                    print('{} becomes {}'.format(k, v))
                    user['address'][k] = v
                    put_address = True
    except:
        pass

    if put_user is True:
        # print(user)
        params = {}
        for k in user:
            if k not in {'details', 'address', 'favorites', 'id', 'public_id'}:
                params[k] = user[k]
        print(params)
        db.session.query(User).filter_by(
            public_id=public_id).update(params)
        # db.session.commit()

    if put_address is True:
        params = {}
        for k in user['address']:
            if k not in {'user', 'id'}:
                params[k] = user['address'][k]
        print(params)
        db.session.query(Address).filter_by(user_id=u.id).update(params)
        # db.session.commit()

    if put_details is True:
        params = {}
        for k in user['details']:
            if k not in {'user', 'id'}:
                params[k] = user['details'][k]
        print(params)
        db.session.query(Details).filter_by(user_id=u.id).update(params)

    if put_user is True or put_address is True or put_details is True:
        db.session.commit()
    return None


def create_recipe(self, data):
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


def update_recipe(self, public_id, data):
    exclude = {'ingredients', 'instructions'}
    r = Recipe.query.filter_by(public_id=public_id).first()
    recipe = RecipeSchema().dump(r).data
    data
    put_recipe = False
    put_ingredient = False
    put_instruction = False
    for k, v in data.items():
        if k in recipe and k not in exclude:
            if recipe.get(k) is not v:
                recipe[k] = v
                put_recipe = True

    ingredient_params = []
    try:
        if data['ingredients']:
            for ingredient in data['ingredients']:
                if 'id' not in ingredient:
                    new_ingredient = Ingredient(
                        **{k: v for k, v in ingredient.items()
                            if k in {'unit', 'product', 'quantity'}}
                    )
                    new_ingredient.recipe = r
                    db.session.add(new_ingredient)
                for original in recipe['ingredients']:
                    if ingredient['id'] is original['id']:
                        params = {}
                        for k, v in ingredient.items():
                            if k in original and original[k] != v:
                                params[k] = v
                        if bool(params):
                            params['id'] = original['id']
                        ingredient_params.append(params)
    except:
        pass
    for d in ingredient_params:
        if 'id' in d:
            db.session.query(Ingredient).filter_by(id=d['id']).update(d)

    instruction_params = []
    try:
        if data['instructions']:
            for instruction in data['instructions']:
                if 'id' not in instruction:
                    new_instruction = Instruction(
                        **{k: v for k, v in instruction.items()
                            if k in {'instruction', 'step'}}
                    )
                    new_instruction.recipe = r
                    db.session.add(new_instruction)
                for original in recipe['instructions']:
                    if instruction['id'] is original['id']:
                        params = {}
                        for k, v in instruction.items():
                            if k in original and original[k] != v:
                                params[k] = v
                        if bool(params):
                            params['id'] = original['id']
                        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                        # So apparently this is a bug...
                        # Adding update instructions withing a loop within a try/except block will kill the loop
                        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                        # db.session.query(Instruction).filter_by(id=instruction['id']).update(params)
                        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                        instruction_params.append(params)
    except:
        pass
    for d in instruction_params:
        if 'id' in d:
            db.session.query(Instruction).filter_by(id=d['id']).update(d)
    db.session.commit()
