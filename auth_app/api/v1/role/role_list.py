import http

from flask_jwt_extended import jwt_required
from flask_restful import Resource

from api.v1.utils.decorators import token_not_in_block_list
from models.db_models import Role
from schemas.role import MultipleRolesSchema


class RoleList(Resource):
    @jwt_required()
    @token_not_in_block_list()
    def get(self):
        """
        Method to get all roles
        ---
        tags:
          - role
        responses:
          200:
            description: Get all roles in DB
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                    description: PK role type
                  role_type:
                    type: string
                    description: Name role type
        """
        roles = Role.query.all()
        return MultipleRolesSchema.dump(roles), http.HTTPStatus.OK
