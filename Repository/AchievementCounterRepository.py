from models import AchievementsCounter, ScoreMontly
from app import db
from .AchievementRepository import AchievementRepository


class AchievementCounterRepository:

    def __init__(self):
        self.achievement_repo = AchievementRepository()

    def update_counter(self, user_id, type_of_product, quantity):
        instance = db.session.query(AchievementsCounter).filter_by(user_id=user_id).first()
        score = db.session.query(ScoreMontly).filter_by(user_id=user_id).first()

        if not score:
            score = ScoreMontly()
            score.user_id = user_id
            score.score = 0

        if not instance:
            instance = AchievementsCounter()
            instance.user_id = user_id
            instance.has_bike = 0
            instance.rent_bike_counter = 0
            instance.parking_counter = 0

        if type_of_product == 'bike_purchase':
            instance.has_bike += quantity
            score.score += 50
            self.achievement_repo.assign_achievement(user_id, type_of_product, instance.has_bike)
        elif type_of_product == 'bike_renting':
            score.score += 5
            instance.rent_bike_counter += quantity
            print(instance.rent_bike_counter)
            self.achievement_repo.assign_achievement(user_id, type_of_product, instance.rent_bike_counter)
        elif type_of_product == 'park_renting':
            score.score += 1
            instance.parking_counter += quantity
            self.achievement_repo.assign_achievement(user_id, type_of_product, instance.parking_counter)

        db.session.add(score)
        db.session.commit()

        db.session.add(instance)
        db.session.commit()

        return {'message': 'The counter has been increased'}, 200
