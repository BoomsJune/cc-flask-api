from flask import Blueprint

from api.schemas import parser, response_ok, response_err


bp = Blueprint("index", __name__, url_prefix="index")


@bp.route("", methods=["GET"])
def index():
    """index"""
    return response_ok("ok")
