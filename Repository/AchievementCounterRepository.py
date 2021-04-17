from models import Achievements, ScoreMontly
from app import db
from AchievementRepository import AchievementRepository


class AchievementCounterRepository:

    def __init__(self):
        self.achievement_repo = AchievementRepository()

    def update_counter(self, user_id, type_of_product, quantity):
        instance = db.session.query(Achievements).filter_by(user_id=user_id).first()
        score = db.session.query(ScoreMontly).filter_by(user_id=user_id).first()

        if not score:
            score = ScoreMontly()

        if not instance:
            instance = Achievements()

        # TODO Get names
        if type_of_product == 'bike_purchase':
            instance.has_bike = instance.has_bike + quantity
            score.score = score.score + 50
            self.achievement_repo.assign_achievement(user_id, type_of_product, instance.has_bike)
        elif type_of_product == 'bike_renting':
            score.score = score.score + 5
            instance.rent_bike_counter = instance.rent_bike_counter + quantity
            self.achievement_repo.assign_achievement(user_id, type_of_product, instance.rent_bike_counter)
        elif type_of_product == 'park_renting':
            score.score = score.score + 1
            instance.parking_counter = instance.parking_counter + quantity
            self.achievement_repo.assign_achievement(user_id, type_of_product, instance.parking_counter)

        db.session.add(score)
        db.session.commit()

        db.session.add(instance)
        db.session.commit()

        return instance
