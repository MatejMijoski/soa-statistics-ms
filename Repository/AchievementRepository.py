from marshmallow import Schema, fields
from models import Achievements, AchievementHelper
from app import db


class AchievementSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    achievement_id = fields.Integer()


schema = AchievementSchema()


def achievement_result(achievement):
    result = dict(id=achievement.id, user_id=achievement.user_id, achievement_id=achievement.achievement_id)
    return schema.dump(result)


class AchievementRepository:

    def __init__(self):
        pass

    def create_achievement(self, achievement):
        db.session.add(achievement)
        db.session.commit()
        return achievement_result(achievement)

    def assign_achievement(self, user_id, type_of_product, quantity):
        achievement = Achievements()
        achievement.user_id = user_id
        if type_of_product == 'bike_purchase':
            if quantity == 1:
                achievement_name = "BronzeBuyingMedal"
            elif quantity == 5:
                achievement_name = "SilverBuyingMedal"
            elif quantity == 10:
                achievement_name = "GoldBuyingMedal"
        elif type_of_product == 'bike_renting':
            if quantity == 5:
                achievement_name = "BronzeRentingMedal"
            elif quantity == 10:
                achievement_name = "SilverRentingMedal"
            elif quantity == 25:
                    achievement_name = "GoldRentingMedal"
        elif type_of_product == 'park_renting':
            if quantity == 5:
                achievement_name = "BronzeParkingMedal"
            elif quantity == 10:
                achievement_name = "SilverParkingMedal"
            elif quantity == 25:
                achievement_name = "GoldParkingMedal"

        achievement_helper = db.session.query(AchievementHelper).filter_by(
            achievement_name=achievement_name).first()
        achievement.achievement_id = achievement_helper
        db.session.add(achievement)
        db.session.commit()
        return achievement_result(achievement)

    def get_achievement_user(self, user_id):
        achievements = db.session.query(Achievements).filter_by(user_id=user_id).all()

        if achievements:
            return achievement_result(achievements)
        else:
            return {'error': 'Achievement for user with ID {} not found'.format(id)}, 404
