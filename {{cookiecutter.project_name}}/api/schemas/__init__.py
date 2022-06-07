from flask import Response, jsonify
from marshmallow import EXCLUDE, Schema, fields
from webargs.flaskparser import FlaskParser


class Parser(FlaskParser):
    """参数解析"""

    # 存在不明参数默认为抛异常 修改为直接弃掉，
    DEFAULT_UNKNOWN_BY_LOCATION = {
        "query": EXCLUDE,
        "form": EXCLUDE,
        "json": EXCLUDE,
    }


parser = Parser()


class PageArg(Schema):
    """分页默认参数"""

    sort = fields.List(fields.Str(), missing=[])  # 排序
    current = fields.Int(missing=1)  # 当前页
    page_size = fields.Int(data_key="pageSize", missing=20)  # 最大页数


def response_ok(data=None, msg="ok", code=0) -> Response:
    """响应成功格式化

    Args:
        data (Any, optional): 数据. Defaults to None.
        msg (str, optional): 成功消息. Defaults to "ok".
        code (int, optional): 成功标识. Defaults to 0.

    Returns:
        Response: flask.Response
    """
    if data is None:
        data = {}
    return jsonify(
        {
            "code": code,
            "msg": msg,
            "data": data,
        }
    )


def response_err(msg="server error", code=-1, status_code=200) -> Response:
    """响应失败格式化

    Args:
        msg (str, optional): 失败消息. Defaults to "server error".
        code (int, optional): 失败标识. Defaults to -1.
        status_code (int, optional): HTTP 状态码. Defaults to 200.

    Returns:
        Response: flask.Response
    """
    return (
        jsonify(
            {
                "code": code,
                "msg": msg,
            }
        ),
        status_code,
    )
