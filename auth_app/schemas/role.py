from marshmallow import Schema, fields

from marshm import ma
from models import Role, Permission, RolePermission


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "role_type")
        model = Role


class PermissionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "permission_type")
        model = Permission


class RolePermissionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "role_id", "permission_id")
        model = RolePermission


class UserRoleSchema(Schema):
    user_id = fields.UUID(allow_none=False, required=True)
    role_id = fields.UUID(allow_none=False, required=True)


class RoleUpdateSchema(ma.Schema):
    id = fields.UUID(allow_none=False, required=True)
    name = fields.String(allow_none=False, required=True)


SingleRoleSchema = RoleSchema()
MultipleRolesSchema = RoleSchema(many=True)

SinglePermissionSchema = PermissionSchema()
MultiplePermissionsSchema = PermissionSchema(many=True)

SingleRolePermissionSchema = RolePermissionSchema()
MultipleRolePermissionSchema = RolePermissionSchema(many=True)

SingleUserRoleSchema = UserRoleSchema()
