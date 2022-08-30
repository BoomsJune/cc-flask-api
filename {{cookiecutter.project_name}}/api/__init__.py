from flask import Flask
from flask_cors import CORS

import api.router as router
import api.exception as exception
from api.extensions import jwt, db, celery, log


def create_app(test_config: dict = None) -> Flask:
    """创建Flask应用

    Args:
        test_config (dict, optional): 测试用配置. Defaults to None.

    Returns:
        Flask: flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    # load config
    app.config.from_prefixed_env()
    import api.config as config

    app.config.from_object(config)
    if test_config:
        app.config.from_mapping(test_config)

    router.init_app(app)
    log.init_app(app)
    exception.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    celery.init_app(app)

    CORS(app)

    return app
