from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()


def init_app(app):
    """初始化数据库"""
    db.init_app(app)
    Migrate(app, db, compare_type=True)
