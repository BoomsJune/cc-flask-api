import logging

from flask import has_request_context, request
from flask.logging import default_handler
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


class RequestFormatter(logging.Formatter):
    """请求日志格式化"""

    def format(self, record) -> str:
        fields = [
            "url",
            "method",
            "remote_addr",
            "user_agent",
            "data",
            "content_type",
            "content_length",
        ]
        if has_request_context():
            for f in fields:
                setattr(record, f, getattr(request, f, None))
        else:
            for f in fields:
                setattr(record, f, "-")
        return super().format(record)


def init_app(app):
    """日志初始化"""
    formatter = RequestFormatter(
        "[%(levelname)s] %(asctime)s %(remote_addr)s %(method)s %(url)s "
        "%(data)s %(content_length)s %(content_type)s %(user_agent)s "
        "%(filename)s %(lineno)d: %(message)s"
    )
    default_handler.setFormatter(formatter)

    print(app.config.get("FLASK_DEBUG"))
    if app.config.get("FLASK_DEBUG"):
        app.logger.info("here")
        sentry_sdk.init(app.config.get("SENTRY_DSN"), integrations=[FlaskIntegration()])
