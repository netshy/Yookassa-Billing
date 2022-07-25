import http

from flask import make_response, jsonify, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from api.v1.utils.decorators import token_not_in_block_list, admin_permission
from db.db import sql_db
from models.db_models import UserRole
from schemas.role import UserRoleSchema, SingleUserRoleSchema


class RoleUserSet(Resource):
    @jwt_required()
    @admin_permission()
    @token_not_in_block_list()
    def post(self):
        """
        Method to set user permission
        ---
        tags:
          - role
        parameters:
          - in: body
            name: body
            schema:
              id: RoleUserSet
              required:
                - user_id
                - role_id
              properties:
                user_id:
                  type: string
                  description: User PK.
                role_id:
                  type: string
                  description: Role PK.
        responses:
          201:
            description: Response after set user permission
            schema:
              type: object
              properties:
                user_id:
                  type: string
                  description: User PK
                role_id:
                  type: string
                  description: Role PK
        """
        try:
            data = UserRoleSchema().load(request.get_json())
        except ValidationError as error:
            make_response(jsonify(msg=str(error)), http.HTTPStatus.BAD_REQUEST)
        is_relation_exist = UserRole.is_user_role_exist(
            user_id=data["user_id"], role_id=data["role_id"]
        )
        if is_relation_exist:
            return make_response(
                jsonify(
                    msg=(
                        f"user_role relation user_id: {data['user_id']},"
                        f" role_id: {data['role_id']} already exist"
                    )
                ),
                http.HTTPStatus.BAD_REQUEST,
            )

        new_user_role = UserRole(
            user_id=data["user_id"], role_id=data["role_id"]
        )
        try:
            sql_db.session.add(new_user_role)
            sql_db.session.commit()
            return (
                SingleUserRoleSchema.dump(new_user_role),
                http.HTTPStatus.CREATED,
            )
        except IntegrityError as error:
            sql_db.session.rollback()
            make_response(jsonify(msg=str(error)), http.HTTPStatus.BAD_REQUEST)
