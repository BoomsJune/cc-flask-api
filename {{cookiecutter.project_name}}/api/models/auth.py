from flask import current_app

from ._base import BaseModel
from api.extensions.db import db
from api.util import now_ts, md5


class AuthUser(BaseModel):
    """用户"""

    __tablename__ = "auth_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(
        db.String(64), unique=True, nullable=False, default=""
    )  # 用户名
    password = db.Column(db.String(32), nullable=False, default="")  # 密码
    created_ts = db.Column(db.Integer, nullable=False)  # 创建时间戳

    def __init__(self, **kwargs):
        self.created_ts = now_ts()
        super().__init__(**kwargs)

    def create(self):
        self.password = self.hash_password(self.password)
        return super().create()

    @classmethod
    def hash_password(cls, password: str):
        """哈希密码"""
        key = current_app.config.get("SECRET_KEY")
        return md5(f"{password}&{key}")

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
