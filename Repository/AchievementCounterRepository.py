from models import Achievements
from app import db

class AchievementCounterRepository:
    def get_or_create_counter(self, user_id):
        instance = db.session.query(Achievements).filter_by(user_id=user_id).first()
        if instance:
            return instance
        else:
            achievement = Achievements()
            db.session.add(achievement)
            db.session.commit()
            return achievement
