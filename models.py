from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:' + os.environ.get('PASSWORD') + '@localhost:5433/statistics-ms'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Achievements_Helper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    achievement_name = db.Column(db.String(120), nullable=False)

class Achievements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    achievement_id = db.Column(db.String(120), nullable=False)

class AchievementsCounter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    has_bike = db.Column(db.Integer, nullable=False)
    rent_bike_counter = db.Column(db.Integer, nullable=False)
    parking_counter = db.Column(db.Integer, nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    items_sold = db.Column(db.Integer, nullable=False)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())