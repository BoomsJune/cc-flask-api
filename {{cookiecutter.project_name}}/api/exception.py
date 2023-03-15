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
    """API自定义异常"""

    def __init__(self, description: str = None, code: int = BadRequest.code, err: Exception = None):
        super().__init__()
        if description is not None:
            self.description = description

        if code is not None:
            self.code = code

        if err is not None:
            current_app.logger.error(err)


class RequestAPIError(Exception):
    """request api请求异常"""

    def __init__(self, response: requests.Response) -> None:
        self.method = response.request.method
        self.url = response.request.url
        self.req_body = str(response.request.body)
        self.http_code = response.status_code
        self.resp_body = response.text

        super().__init__(f"Failed to {self.method} {self.url} {self.req_body}: [{self.http_code}]{self.resp_body}")


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
        desc = messages.get("json", messages.get("query", messages.get("form", messages.get("files", {}))))
        return response_err(json.dumps(desc), e.code, e.code)
