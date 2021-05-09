import os
from functools import wraps

import connexion
import jwt
from flask import request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

SECRET = 'SECRET_KEY'


def has_role(arg):
    def has_role_inner(fn):
        @wraps(fn)
        def decode_view(*args, **kwargs):
            try:
                headers = request.headers
                if 'Authorization' in headers:
                    token = headers['Authorization'].split(' ')[1]
                    decoded_token = decode_token(token)
                    if 'admin' in decoded_token:
                        return fn(*args, **kwargs)
                    for role in arg:
                        if role in decoded_token['roles']:
                            return fn(*args, **kwargs)
                    abort(404)
                return fn(*args, **kwargs)
            except Exception as e:
                abort(401)

        return decode_view

    return has_role_inner


def decode_token(token):
    return jwt.decode(token, SECRET, algorithms='HS256')


# Get new invoice data
# @has_role(['invoices'])
def new_invoice(invoice_body):
    product_service.update_product(invoice_body)
    return achievement_service.update_achievement(invoice_body)


# @has_role(['discount'])
def get_achievement_user(user_id):
    return achievement_service.get_achievement(user_id)


def get_monthly_score(limit=5):
    return score_service.get_monthly_score(limit)


def get_yearly_score(limit=5):
    return score_service.get_yearly_score(limit)


# @has_role(['discount'])
def get_top_monthly_products(limit=5):
    return product_service.get_top_monthly_products(limit)


# @has_role(['discount'])
def get_end_monthly_products(limit=5):
    return product_service.get_top_monthly_products(limit)


# @has_role(['discount'])
def get_top_yearly_products(limit=5):
    return product_service.get_top_yearly_products(limit)


# @has_role(['discount'])
def get_end_yearly_products(limit=5):
    return product_service.get_end_yearly_products(limit)


c_app = connexion.FlaskApp(__name__, specification_dir='./')
app = c_app.app
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
c_app.add_api('api.yml')

from Services.AchievementService import AchievementService
from Services.ProductService import ProductService
from Services.ScoreService import ScoreService

achievement_service = AchievementService()
product_service = ProductService()
score_service = ScoreService()

if __name__ == "__main__":
    c_app.run(host='127.0.0.1', port=8000, debug=True)
