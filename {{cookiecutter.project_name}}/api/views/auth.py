from flask import Blueprint, current_app

from api.schemas import parser, response_ok, response_err, paginate_resp, auth
from api.models import AuthUser


bp = Blueprint("auth", __name__, url_prefix="auth")


@bp.route("/user_list", methods=["GET"])
@parser.use_args(auth.UserListReq, location="query")
def user_list(args):
    """用户列表查询"""
    from api.exception import APIException

    try:
        1 / 0
    except Exception as e:
        raise APIException("errrrrrr", err=e)

    p = AuthUser.get_by_page(**args)
    data = paginate_resp(auth.UserSchema)().dump(p)
    return response_ok(data)
