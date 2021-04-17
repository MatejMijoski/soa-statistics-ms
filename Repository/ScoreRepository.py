from datetime import datetime

from marshmallow import Schema, fields
from sqlalchemy import and_, func, desc

from models import ScoreMontly, ScoreYearly
from app import db


class ScoreSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    score = fields.Integer()


schema = ScoreSchema()


def score_result(score):
    result = dict(id=score.id, user_id=score.user_id, achievement_id=score.score)
    return schema.dump(result)


class ScoreRepository:

    def __init__(self):
        pass

    def get_monthly_score(self, limit=5):
        instance = db.session.query(ScoreMontly, func.sum(ScoreMontly.score).label("score")) \
                                    .order_by(desc("score")) \
                                    .limit(limit) \
                                    .all()
        if instance:
            return score_result(instance)
        else:
            return {'error': 'No scores were found'}, 404

    def get_yearly_score(self, limit=5):
        instance = db.session.query(ScoreYearly, func.sum(ScoreYearly.score).label("score")) \
                                    .order_by(desc("score")) \
                                    .limit(limit) \
                                    .all()
        if instance:
            return score_result(instance)
        else:
            return {'error': 'No scores were found'}, 404


from apscheduler.schedulers.background import BackgroundScheduler

def restart_score():
    instance = db.session.query(ScoreMontly).all()
    for obj in instance:
        yearly_score = db.session.query(ScoreYearly).filter(user_id=instance.user_id).first()
        if not yearly_score:
            yearly_score = ScoreYearly()
        yearly_score.score = yearly_score.score + obj.score

        db.session.add(yearly_score)
        db.session.delete(obj)
        db.session.commit()

def restart_products():
    instance = db.session.query(ScoreMontly).all()
    for obj in instance:
        yearly_score = db.session.query(ScoreYearly).filter(user_id=instance.user_id).first()
        if not yearly_score:
            yearly_score = ScoreYearly()
        yearly_score.score = yearly_score.score + obj.score

        db.session.add(yearly_score)
        db.session.delete(obj)
        db.session.commit()

sched = BackgroundScheduler(daemon=True)
sched.add_job(restart_score, trigger='cron', day='last')
sched.start()
