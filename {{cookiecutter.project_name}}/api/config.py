import os
import datetime


DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1")

# key
SECRET_KEY = os.getenv("SECRET_KEY", "development_key")
SIGN_SECRET_KEY = os.getenv("SIGN_SECRET_KEY", "development_key")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "development_key")

# log
SENTRY_DSN = os.getenv("SENTRY_DSN", "")

# db
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "")
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv(
    "SQLALCHEMY_TRACK_MODIFICATIONS", "False"
).lower() in ("true", "1")
SQLALCHEMY_BINDS = {
    # "gamedb": os.getenv("SQLALCHEMY_BINDS_GAMEDB", ""),
}

# upload
UPLOAD_PATH = os.getenv(
    "UPLOAD_PATH", os.path.join(os.path.abspath(os.curdir), "instance/upload")
)

# celery
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379")
CELERY_RESULT_BACKEND = os.getenv(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)
CELERYBEAT_SCHEDULE = {
    "index": {
        "task": "api.tasks.index.index",
        "schedule": datetime.timedelta(minutes=5),
    },
}

# jwt
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)
