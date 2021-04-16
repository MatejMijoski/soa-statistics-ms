from marshmallow import Schema, fields
from models import Achievements
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

    def get_achievement_by_id(self, id):
        achievement = db.session.query(Achievements).filter_by(id=id).first()

        if achievement:
            return achievement_result(achievement)
        else:
            return {'error': 'Achievement with id {} not found'.format(id)}, 404
