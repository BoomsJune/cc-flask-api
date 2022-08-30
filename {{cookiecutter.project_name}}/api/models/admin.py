from __future__ import annotations

from flask import current_app
from flask_jwt_extended import current_user
from sqlalchemy.dialects.postgresql import JSON

from ._mixin import db, CRUDMixin
from api.util import now_ts, md5


class AuthUser(CRUDMixin):
    """用户"""

    __tablename__ = "auth_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False, comment="用户名")
    password = db.Column(db.String(32), nullable=False, default="", comment="密码")
    is_active = db.Column(
        db.SmallInteger, nullable=False, default=1, comment="是否可用"
    )  # 0不可用，1可用
    created_ts = db.Column(db.Integer, nullable=False, comment="创建时间戳")
    created_by = db.Column(db.Integer, nullable=False, comment="创建人")

    def __init__(self, **kwargs):
        self.created_ts = now_ts()
        self.created_by = current_user if current_user else 0
        super().__init__(**kwargs)

    def create(self) -> AuthUser:
        self.password = self.hash_password(self.password)
        return super().create()

    @classmethod
    def hash_password(cls, password: str) -> str:
        """哈希密码"""
        key = current_app.config["SECRET_KEY"]
        return md5(f"{password}&{key}")

    @classmethod
    def get_by_name(cls, name) -> AuthUser:
        return cls.query.filter_by(name=name).first()


class OperateLog(CRUDMixin):
    """系统操作日志"""

    __tablename__ = "operate_log"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    operate = db.Column(db.String(32), nullable=False, default="", comment="操作")
    model = db.Column(
        db.String(32), nullable=False, default="", index=True, comment="数据模型"
    )
    model_key = db.Column(db.String(64), nullable=False, index=True, comment="模型唯一键")
    diff_values = db.Column(JSON, nullable=False, default="{}", comment="变更的数据")
    endpoint = db.Column(db.String(32), nullable=False, default="", comment="路由标识")
    note = db.Column(
        db.String(128), nullable=False, comment="备注"
    )  # 默认为model的__repr__()
    request_method = db.Column(db.String(16), nullable=False, comment="请求方法")
    request_path = db.Column(db.String(16), nullable=False, comment="请求路径")
    is_succeed = db.Column(db.SmallInteger, nullable=False, default=0, comment="是否成功")

    created_ts = db.Column(db.Integer, nullable=False, comment="创建时间戳")
    created_by = db.Column(db.Integer, nullable=False, comment="创建人")

    def __init__(self, **kwargs):
        self.created_ts = now_ts()
        self.created_by = current_user.id if current_user else 0
        super().__init__(**kwargs)
