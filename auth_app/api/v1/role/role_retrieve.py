import http

from flask import make_response, jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from api.v1.utils.decorators import token_not_in_block_list
from models.db_models import Role
from schemas.role import SingleRoleSchema


class RoleRetrieve(Resource):
    @jwt_required()
    @token_not_in_block_list()
    def get(self, role_id):
        """
        Method to get one role by id
        ---
        tags:
          - role
        parameters:
          - in: path
            name: role_id
            required:
              - role_id
            properties:
              role_id:
                type: string
                description: Role PK.
        responses:
          200:
            description: Get one role
            schema:
              properties:
                id:
                  type: string
                  description: Role PK
                role_type:
                  type: string
                  description: Role name
        """
        role = Role.query.filter_by(id=role_id).first()
        if not role:
            return make_response(
                jsonify(msg=f"Role {role_id} not found"),
                http.HTTPStatus.BAD_REQUEST,
            )
        return SingleRoleSchema.dump(role), http.HTTPStatus.OK
