import json
import requests

from flask import current_app
from werkzeug.exceptions import (
    HTTPException,
    BadRequest,
    UnprocessableEntity,
    Unauthorized,
    Forbidden,
)

from api.schemas import response_err


class APIException(HTTPException):
    """api自定义异常，统一由flask处理响应

    Args:
        description (str): 异常描述
        code (int): 异常标识
    """

    def __init__(self, description: str = None, code: int = BadRequest.code):
        super().__init__()
        if description is not None:
            self.description = description

        if code is not None:
            self.code = code


class RequestAPIError(Exception):
    """request api请求异常"""

    def __init__(self, response: requests.Response) -> None:
        super().__init__(response)
        self.response = response
        info = {
            "method": response.request.method,
            "url": response.request.url,
            "params": response.request.body,
            "http_code": response.status_code,
            "body": response.text,
        }
        current_app.logger.error(json.dumps(info))


def init_app(app):
    """异常处理初始化"""

    @app.errorhandler(APIException)
    def handle_api_exception(e):
        return response_err(e.description, e.code)

    @app.errorhandler(Unauthorized)
    def handle_unauthorized(e):
        return response_err(e.description, e.code)

    @app.errorhandler(Forbidden)
    def handle_forbidden(e):
        return response_err(e.description, e.code)

    @app.errorhandler(UnprocessableEntity)
    def handle_unprocessable_entity(e):
        messages = e.data.get("messages")
        desc = messages.get(
            "json",
            messages.get("query", messages.get("form", messages.get("files", {}))),
        )
        return response_err(json.dumps(desc), e.code, e.code)
