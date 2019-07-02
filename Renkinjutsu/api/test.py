from api import db
from models.user import *
from models.recipe import *
from werkzeug.security import generate_password_hash
import uuid

password = 'alpine12'
hash_password = generate_password_hash(password, method='sha256')

admin = User(public_id=str(uuid.uuid4()),
             username='Admin',
             password=hash_password,
             admin=True)

admin_address = Address(streetname='Lunettenhof',
                        house_number='56',
                        zip_code='9723KA',
                        city='Groningen',
                        user=admin)

admin_details = Details(first_name='Kyle',
                        last_name='Gravenhorst',
                        gender='male',
                        date_of_birth='1989-07-27',
                        height='175',
                        weight='60',
                        e_mail_address='k.t.c.gravenhorst@st.hanze.nl',
                        phone_number='+31634347875',
                        user=admin)


def test_data():
    db.session.add(admin)
    db.session.add(admin_address)
    db.session.add(admin_details)
    db.session.commit()


test_dish = Recipe(public_id=str(uuid.uuid4()),
                   dish='Broodje kaas',
                   description='Een dubbele bruine boterham met boter en kaas',
                   calories='127')

ingredients = [
    Ingredient(product='Kaas',
               quantity='20',
               unit='Gram',
               recipe=test_dish),
    Ingredient(product='Brood',
               quantity='2',
               unit='Plakken',
               recipe=test_dish),
    Ingredient(product='Boter',
               recipe=test_dish)
]


def test_recipe():
    db.session.add(test_dish)
    for ingredient in ingredients:
        db.session.add(ingredient)
    db.session.commit()


def test_all():
    test_data()
    test_recipe()
