from flask_jwt_extended import JWTManager
from werkzeug.exceptions import Unauthorized

from api.schemas import response_err
from api.models import AuthUser


jwt = JWTManager()


def init_app(app):
    """初始化jwt"""
    jwt.init_app(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(jwt_header, jwt_data):
        identity = jwt_data.get("sub")

        user = AuthUser.query.get(identity)
        if user and user.is_active:
            return user

        return None

    @jwt.user_lookup_error_loader
    def user_lookup_error_loader_callback(header, payload):
        return response_err("用户不可用", Unauthorized.code, Unauthorized.code)

    @jwt.unauthorized_loader
    def custom_unauthorized_request_callback(error_context):
        return response_err("用户未登录", Unauthorized.code, Unauthorized.code)

    @jwt.revoked_token_loader
    def custom_revoked_token_callback():
        return response_err("用户未登录", Unauthorized.code, Unauthorized.code)

    @jwt.expired_token_loader
    def custom_expired_token_callback(jwt_header, jwt_payload):
        return response_err("请求令牌已过期", Unauthorized.code, Unauthorized.code)

    @jwt.invalid_token_loader
    def custom_invalid_token_callback(error_context):
        return response_err("无效的请求令牌", Unauthorized.code, Unauthorized.code)
