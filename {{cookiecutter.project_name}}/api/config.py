import os
import datetime


def to_bool(s: str) -> bool:
    return s.lower() in ("true", "1")


# log
SENTRY_DSN = os.getenv("SENTRY_DSN", "")


# db
SQLALCHEMY_ECHO = to_bool(os.getenv("SQLALCHEMY_ECHO", "False"))  # 打印所有执行的SQL
SQLALCHEMY_TRACK_MODIFICATIONS = to_bool(os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False"))  # 追踪修改并发出signal，耗内存
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "")  # 默认连接的数据库
SQLALCHEMY_BINDS = {  # 指定bind_key连接的数据库
    # "gamedb": os.getenv("SQLALCHEMY_BINDS_GAMEDB", ""),
}


# redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


# celery
CELERY_CONFIG = {
    "broker_url": os.getenv("CELERY_BROKER_URL", "redis://localhost:6379"),
    "result_backend": os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379"),
    "beat_schedule": {
        "index": {
            "task": "api.tasks.index.index",
            "schedule": datetime.timedelta(seconds=10),
        },
    },
}


# jwt
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "development_key")
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)
