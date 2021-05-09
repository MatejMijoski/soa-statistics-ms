import requests
from consul import Consul
from marshmallow import Schema, fields
from models import Achievements, AchievementHelper
from app import db
from flask import request, abort


class AchievementSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    achievement_id = fields.Integer()


schema = AchievementSchema()


def achievement_result(achievement):
    result = dict(id=achievement.id, user_id=achievement.user_id, achievement_id=achievement.achievement_name)
    return schema.dump(result)


class AchievementRepository:

    def create_achievement(self, achievement):
        db.session.add(achievement)
        db.session.commit()
        return achievement_result(achievement)

    def assign_achievement(self, user_id, type_of_product, counter):
        achievement_name = None
        achievement = Achievements()
        achievement.user_id = user_id
        if type_of_product == 'bike_purchase':
            if counter == 1:
                achievement_name = "BronzeBuyingMedal"
            elif counter == 5:
                achievement_name = "SilverBuyingMedal"
            elif counter == 10:
                achievement_name = "GoldBuyingMedal"
        elif type_of_product == 'bike_renting':
            if counter == 5:
                achievement_name = "BronzeRentingMedal"
            elif counter == 10:
                achievement_name = "SilverRentingMedal"
            elif counter == 25:
                achievement_name = "GoldRentingMedal"
        elif type_of_product == 'park_renting':
            if counter == 5:
                achievement_name = "BronzeParkingMedal"
            elif counter == 10:
                achievement_name = "SilverParkingMedal"
            elif counter == 25:
                achievement_name = "GoldParkingMedal"

        if achievement_name != "":
            consul = Consul(host="consul", port=8500)
            agent = consul.agent
            service_list = agent.services()
            service_info = service_list["discounts"]
            url = "{}:{}/api/postUserRank/{}/".format(service_info['Address'], service_info['Port'], user_id)

            headers = request.headers
            auth_headers = {}
            if 'Authorization' in headers:
                auth_headers["Authorization"] = headers['Authorization']
            discounts_response = requests.post(url=url, headers=auth_headers, json={"discountRank_type": achievement_name})
            achievement.achievement_name = achievement_name
            db.session.add(achievement)
            db.session.commit()
            return achievement_result(achievement)

    def get_achievement_user(self, user_id):
        achievements = db.session.query(Achievements).filter_by(user_id=user_id).all()

        if achievements:
            return achievement_result(achievements)
        else:
            return {'error': 'Achievement for user with ID {} not found'.format(id)}, 404
