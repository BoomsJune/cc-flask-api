from marshmallow import Schema, fields, validate

from . import PaginateReq


class UserSchema(Schema):
    """用户"""

    id = fields.Int()
    username = fields.Str()


class UserListReq(PaginateReq):
    """用户列表查询参数"""

    search = fields.Str()


class UserFormReq(Schema):
    """用户表单参数"""

    id = fields.Int()
    username = fields.Str(required=True, validate=validate.Length(max=64))
    password = fields.Str(
        required=True, validate=validate.Length(max=32), data_key="nickName"
    )
    is_active = fields.Int(required=True, data_key="isActive")
    roles = fields.List(fields.Str())
