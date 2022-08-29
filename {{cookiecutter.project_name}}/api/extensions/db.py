from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_redis import FlaskRedis


db = SQLAlchemy()
redis_client = FlaskRedis(decode_responses=True)


def init_app(app):
    """初始化数据库"""
    db.init_app(app)
    Migrate(app, db, compare_type=True)

    redis_client.init_app(app)
