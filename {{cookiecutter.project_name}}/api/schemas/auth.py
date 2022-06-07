from marshmallow import Schema, fields, validate

from . import PageArg


class UserSchema(Schema):
    """用户"""

    id = fields.Int()
    name = fields.Str()
    nick_name = fields.Str(data_key="nickName")
    en_name = fields.Str(data_key="enName")
    phone = fields.Str()
    email = fields.Str()
    avatar = fields.Str()
    union_id = fields.Str(data_key="unionId")
    is_active = fields.Int(data_key="isActive")
    roles = fields.List(fields.Str())


class UserQueryArg(PageArg):
    """用户查询参数"""

    search = fields.Str()


class UserFormArg(Schema):
    """用户表单参数"""

    id = fields.Int()
    name = fields.Str(required=True, validate=validate.Length(max=64))
    nick_name = fields.Str(
        required=True, validate=validate.Length(max=32), data_key="nickName"
    )
    is_active = fields.Int(required=True, data_key="isActive")
    roles = fields.List(fields.Str())
