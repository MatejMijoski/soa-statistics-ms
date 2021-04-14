from marshmallow import Schema, fields
from models import db

class Achievement(Schema):
    id=fields.Number()
    user_id=fields.Number()
    achievement_id=fields.Number()

schema=Achievement()

def achievement_Result(achievement):
    result=dict(id=achievement.id, userId=achievement.user_id, achievementId=achievement.achievement_id)
    return schema.dump(result)

class AchievementRepository:
    def create_Achievement(self, achievement):
        db.session.add(achievement)
        db.session.commit()
        return achievement_Result(achievement)

    def get_achievement_by_id(id):
        achievement = db.session.query(Achievement).filter_by(id=id).first()

        if achievement:
            return achievement_Result(achievement)
        else:
            return {'error': 'Achievement with id {} not found'.format(id)}, 404