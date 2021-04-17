from app import db


class AchievementHelper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    achievement_name = db.Column(db.String(120), nullable=False)


class Achievements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    achievement_id = db.Column(db.String(120), db.ForeignKey('achievement_helper.id'), nullable=False)


class AchievementsCounter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, default=0)
    has_bike = db.Column(db.Integer, nullable=False, default=0)
    rent_bike_counter = db.Column(db.Integer, nullable=False, default=0)
    parking_counter = db.Column(db.Integer, nullable=False, default=0)


class ProductMonthly(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    items_sold = db.Column(db.Integer, nullable=False)


class ProductYearly(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    items_sold = db.Column(db.Integer, nullable=False)


class ScoreYearly(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)


class ScoreMontly(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
