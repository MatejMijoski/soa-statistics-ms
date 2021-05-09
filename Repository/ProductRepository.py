from sqlalchemy import func, asc

from models import ProductMonthly, ProductYearly
from app import db

from marshmallow import Schema, fields
from sqlalchemy import desc


class ProductSchema(Schema):
    id = fields.Integer()
    product_id = fields.Integer()
    items_sold = fields.Integer()


schema = ProductSchema()


def product_result(instance):
    result = dict(id=instance.id, product_id=instance.product_id, items_sold=instance.items_sold)
    return schema.dump(result)


class ProductRepository:

    def __init__(self):
        pass

    def update_product_counter(self, product_id, quantity):
        instance = db.session.query(ProductMonthly).filter_by(product_id=product_id).first()
        instance_yearly = db.session.query(ProductYearly).filter_by(product_id=product_id).first()
        if not instance:
            instance = ProductMonthly()
            instance.product_id = product_id
            instance.items_sold = quantity
            db.session.add(instance)
            db.session.commit()
            return product_result(instance)
        elif instance:
            instance.items_sold += quantity
            db.session.add(instance)
            db.session.commit()
            return product_result(instance)
        if not instance_yearly:
            instance_yearly = ProductYearly()
            instance_yearly.product_id = product_id
            instance_yearly.items_sold = quantity
            db.session.add(instance_yearly)
            db.session.commit()
            return product_result(instance_yearly)
        elif instance:
            instance_yearly.items_sold += quantity
            db.session.add(instance_yearly)
            db.session.commit()
            return product_result(instance_yearly)

    def get_top_monthly_products(self, limit=5):
        instances = db.session.query(ProductMonthly) \
            .order_by(desc("items_sold")).limit(limit).all()
        if instances:
            response = []
            for item in instances:
                response.append(product_result(item))
            return response
        else:
            return {'error': 'No scores were found'}, 404

    def get_end_monthly_products(self, limit=5):
        instances = db.session.query(ProductMonthly) \
            .order_by(desc("items_sold")).limit(limit).all()
        if instances:
            response = []
            for item in instances:
                response.append(product_result(item))
            return response
        else:
            return {'error': 'No scores were found'}, 404

    def get_top_yearly_products(self, limit=5):
        instances = db.session.query(ProductMonthly) \
            .order_by(asc("items_sold")).limit(limit).all()
        if instances:
            response = []
            for item in instances:
                response.append(product_result(item))
            return response
        else:
            return {'error': 'No scores were found'}, 404

    def get_end_yearly_products(self, limit=5):
        instances = db.session.query(ProductMonthly) \
            .order_by(asc("items_sold")).limit(limit).all()
        if instances:
            response = []
            for item in instances:
                response.append(product_result(item))
            return response
        else:
            return {'error': 'No scores were found'}, 404


from apscheduler.schedulers.background import BackgroundScheduler


def restart_products():
    instance = db.session.query(ProductMonthly).all()
    for obj in instance:
        yearly_score = db.session.query(ProductYearly).filter(product_id=instance.product_id).first()
        if not yearly_score:
            yearly_score = ProductYearly()
        yearly_score.score = yearly_score.score + obj.score

        db.session.add(yearly_score)
        db.session.delete(obj)
        db.session.commit()


sched = BackgroundScheduler(daemon=True)
sched.add_job(restart_products, trigger='cron', day='last')
sched.start()
