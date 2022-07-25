import http

from flask import make_response, jsonify, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from api.v1.utils.decorators import token_not_in_block_list, admin_permission
from db.db import sql_db
from models.db_models import UserRole
from schemas.role import UserRoleSchema


class RoleUserRemove(Resource):
    @jwt_required()
    @admin_permission()
    @token_not_in_block_list()
    def delete(self):
        """
        Method to remove user permissions
        ---
        tags:
          - role
        parameters:
          - in: body
            name: body
            schema:
              id: RoleUserRemove
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
          200:
            description: Response after remove user permissions
            schema:
              type: object
              properties:
                msg:
                  type: string
                  description: success info after remove permission
        """
        try:
            data = UserRoleSchema().load(request.get_json())
        except ValidationError as error:
            return make_response(
                jsonify(msg=str(error)), http.HTTPStatus.BAD_REQUEST
            )
        existed_role = UserRole.query.filter_by(
            user_id=data["user_id"], role_id=data["role_id"]
        ).first()
        if not existed_role:
            return make_response(
                jsonify(
                    msg=(
                        f"user_role relation user_id: {data['user_id']},"
                        f" role_id: {data['role_id']} doesn't exist"
                    )
                ),
                http.HTTPStatus.NOT_FOUND,
            )
        try:
            sql_db.session.delete(existed_role)
            sql_db.session.commit()
            return make_response(
                jsonify(
                    msg=(
                        f"role_id: {data['role_id']} removed"
                        f" from user_id: {data['user_id']}"
                    )
                ),
                http.HTTPStatus.OK,
            )
        except IntegrityError as error:
            sql_db.session.rollback()
            make_response(jsonify(msg=str(error)), http.HTTPStatus.BAD_REQUEST)
