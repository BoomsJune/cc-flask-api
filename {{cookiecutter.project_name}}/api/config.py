import os
import datetime


# api
SIGN_SECRET_KEY = os.getenv("SIGN_SECRET_KEY", "development_key")
UPLOAD_PATH = os.getenv(
    "UPLOAD_PATH", os.path.join(os.path.abspath(os.curdir), "instance/upload")
)

# log
SENTRY_DSN = os.getenv("SENTRY_DSN", "")

# db
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv(
    "SQLALCHEMY_TRACK_MODIFICATIONS", "False"
).lower() in ("true", "1")
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "")
SQLALCHEMY_BINDS = {
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
