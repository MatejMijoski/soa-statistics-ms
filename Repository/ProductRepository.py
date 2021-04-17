from sqlalchemy import func

from models import ProductMonthly, ProductYearly
from app import db

from marshmallow import Schema, fields
from sqlalchemy import and_, func, desc


class ProductSchema(Schema):
    id = fields.Integer()
    product_id = fields.Integer()
    items_sold = fields.Integer()


schema = ProductSchema()


def product_result(score):
    result = dict(id=score.id, user_id=score.user_id, achievement_id=score.score)
    return schema.dump(result)


class ProductRepository:

    def __init__(self):
        pass

    def update_product_counter(self, product_id, quantity):
        instance = db.session.query(ProductMonthly).filter_by(product_id=product_id).first()
        if not instance:
            instance = ProductMonthly()
        instance.items_sold = instance.items_sold + quantity
        db.session.add(instance)
        db.session.commit()
        return instance

    def get_monthly_score(self, limit=5):
        instance = db.session.query(ProductMonthly, func.sum(ProductMonthly.score).label("score")) \
            .order_by(desc("score")) \
            .limit(limit) \
            .all()
        if instance:
            return product_result(instance)
        else:
            return {'error': 'No scores were found'}, 404

    def get_yearly_score(self, limit=5):
        instance = db.session.query(ProductYearly, func.sum(ProductYearly.score).label("score")) \
            .order_by(desc("score")) \
            .limit(limit) \
            .all()
        if instance:
            return product_result(instance)
        else:
            return {'error': 'No scores were found'}, 404


from apscheduler.schedulers.background import BackgroundScheduler


def restart_products():
    instance = db.session.query(ProductMonthly).all()
    for obj in instance:
        yearly_score = db.session.query(ProductYearly).filter(user_id=instance.user_id).first()
        if not yearly_score:
            yearly_score = ProductYearly()
        yearly_score.score = yearly_score.score + obj.score

        db.session.add(yearly_score)
        db.session.delete(obj)
        db.session.commit()


sched = BackgroundScheduler(daemon=True)
sched.add_job(restart_products, trigger='cron', day='last')
sched.start()
