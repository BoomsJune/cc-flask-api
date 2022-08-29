import pkgutil

from flask import Blueprint, request, current_app

import api.views as views
from api.util import sign_by_md5, now_ts
from api.exception import APIException


def init_app(app):
    """路由初始化"""
    api = Blueprint("api", __name__, url_prefix="/api")
    scan_router(api, views)

    app.before_request_funcs.setdefault(
        None,
        [
            # sign_middleware
        ],
    )
    app.register_blueprint(api)


def scan_router(parent, module):
    """扫描并注册路由"""
    for _, name, _ in pkgutil.iter_modules(
        module.__path__, prefix=module.__name__ + "."
    ):
        blueprint_name = "bp"
        modules = __import__(name, fromlist=["dummy"])
        blueprint = getattr(modules, blueprint_name)
        if isinstance(blueprint, Blueprint):
            parent.register_blueprint(blueprint)


def sign_middleware(expire=60):
    """签名校验中间件"""
    content_type = request.content_type or ""
    headers = request.headers
    nonce = headers.get("_nonce", "")
    ts = headers.get("_ts", "")
    sign = headers.get("_sign", "")

    if not (ts.isdigit() and 0 < now_ts() - int(ts) < expire):
        raise APIException("invalid timestamp", 40001)

    data = {}
    if content_type.startswith("application/json"):
        data = request.json
    elif content_type.startswith("multipart/form-data") or content_type.startswith(
        "application/x-www-form-urlencoded"
    ):
        data = request.form
    else:
        data = request.args

    data = dict(data)
    data.update(
        {
            "nonce": nonce,
            "ts": ts,
        }
    )

    my_sign = sign_by_md5(data, current_app.config.get("SIGN_SECRET_KEY"))
    if sign != my_sign:
        raise APIException("invalid sign", 40000)
