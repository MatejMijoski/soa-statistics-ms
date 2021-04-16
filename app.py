import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


def get_achievement_by_id(achievement_id):
    return achievement_service.get_achievement(achievement_id)


c_app = connexion.FlaskApp(__name__, specification_dir='./')
app = c_app.app
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:' + os.environ.get(
    'PASSWORD') + '@localhost:5433/statistics-ms'
c_app.add_api('api.yml')

from Services.AchievementService import AchievementService
achievement_service = AchievementService()


if __name__ == "__main__":
    c_app.run(host='127.0.0.1', port=8000, debug=True)
