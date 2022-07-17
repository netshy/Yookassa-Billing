import http

from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from api.v1.utils.decorators import token_not_in_block_list, admin_permission
from auth import sql_db
from models.db_models import Role
from schemas.role import RoleSchema, SingleRoleSchema


class RoleCreate(Resource):
    @jwt_required()
    @admin_permission()
    @token_not_in_block_list()
    def post(self):
        """
        Method to create new role
        ---
        tags:
          - role
        parameters:
          - in: body
            name: body
            schema:
              id: RoleCreate
              required:
                - role_type
              properties:
                role_type:
                  type: string
                  description: Role type.
        responses:
          201:
            description: Response after create new role
            schema:
              properties:
                id:
                  type: string
                  description: PK role type
                role_type:
                  type: string
                  description: Name role type
        """
        try:
            data = RoleSchema().load(request.get_json())
            is_role_exists = Role.role_is_exist(data["role_type"])
            if is_role_exists:
                return make_response(
                    jsonify(msg=f"Role {data['role_type']} already exist"),
                    http.HTTPStatus.BAD_REQUEST,
                )
            new_role = Role(role_type=data["role_type"])
            sql_db.session.add(new_role)
            sql_db.session.commit()
            return SingleRoleSchema.dump(new_role), http.HTTPStatus.CREATED
        except ValidationError as error:
            make_response(jsonify(msg=str(error)), http.HTTPStatus.BAD_REQUEST)
        except IntegrityError as error:
            sql_db.session.rollback()
            make_response(jsonify(msg=str(error)), http.HTTPStatus.BAD_REQUEST)
