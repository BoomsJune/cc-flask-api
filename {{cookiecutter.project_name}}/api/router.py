import pkgutil

from flask import Blueprint, request, current_app
from flask_jwt_extended import verify_jwt_in_request

import api.views as views
from api.utils.stringx import sign_by_md5
from api.utils.timex import now_ts
from api.exception import APIException


# 自动扫描路由所需的路由变量名
BLUEPRINT_NAME = "bp"

# 路由前缀
URL_PREFIX = "/api"

# 路由白名单
WHITE_LIST = ["/api/auth/login"]


def init_app(app):
    """路由初始化"""
    api = Blueprint("api", __name__, url_prefix=URL_PREFIX)
    scan_router(api, views)

    app.before_request_funcs.setdefault(
        None,
        [
            # sign_middleware
            auth_middleware
        ],
    )
    app.register_blueprint(api)


def scan_router(parent, module):
    """扫描并注册路由"""
    for _, name, _ in pkgutil.iter_modules(module.__path__, prefix=module.__name__ + "."):
        modules = __import__(name, fromlist=["dummy"])
        blueprint = getattr(modules, BLUEPRINT_NAME)
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
    elif content_type.startswith("multipart/form-data") or content_type.startswith("application/x-www-form-urlencoded"):
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

    my_sign = sign_by_md5(data, current_app.config.get("SECRET_KEY"))
    if sign != my_sign:
        raise APIException("invalid sign", 40000)


def auth_middleware():
    """访问权限验证中间件"""
    path = request.path

    # 在白名单的路由直接通过
    if path in WHITE_LIST:
        return

    verify_jwt_in_request()
