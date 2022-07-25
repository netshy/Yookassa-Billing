from marshmallow import Schema, fields

from marshm import ma
from models import User
from schemas.role import RoleSchema


class UserRegistrationSchema(Schema):
    password_confirmation = fields.String(allow_none=False, required=True)
    password = fields.String(allow_none=False, required=True)
    username = fields.String(allow_none=False, required=True)


class UserUpdateUsernameSchema(Schema):
    username = fields.String(allow_none=False, required=True)


class UserLoginSchema(Schema):
    username = fields.String(allow_none=False, required=True)
    password = fields.String(allow_none=False, required=True)


class UserUpdatePasswordSchema(Schema):
    password = fields.String(allow_none=False, required=True)


class UserSchema(ma.SQLAlchemyAutoSchema):
    roles = ma.Nested(RoleSchema, many=True)

    class Meta:
        model = User


SingleUserSchema = UserSchema()
MultipleUserSchema = UserSchema(many=True)
