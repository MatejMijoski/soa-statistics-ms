import os
import connexion
from flask import Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Get new invoice data
def new_invoice(invoice_body):
    if 'bike_purchase' == invoice_body['type_of_purchase']:
        product_service.update_product(invoice_body)
    return achievement_service.update_achievement(invoice_body)


def get_achievement_user(user_id):
    return achievement_service.get_achievement(user_id)


def get_monthly_score(limit):
    return score_service.get_monthly_score(limit)


def get_yearly_score(limit):
    return score_service.get_yearly_score(limit)


def get_monthly_products(limit):
    return product_service.get_yearly_score(limit)


def get_yearly_products(limit):
    return product_service.get_yearly_score(limit)


c_app = connexion.FlaskApp(__name__, specification_dir='./')
app = c_app.app
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:' + os.environ.get(
    'PASSWORD') + '@localhost:5433/statistics-ms'
c_app.add_api('api.yml')

from Services.AchievementService import AchievementService
from Services.ProductService import ProductService
from Services.ScoreService import ScoreService

achievement_service = AchievementService()
product_service = ProductService()
score_service = ScoreService()

if __name__ == "__main__":
    c_app.run(host='127.0.0.1', port=8000, debug=True)
