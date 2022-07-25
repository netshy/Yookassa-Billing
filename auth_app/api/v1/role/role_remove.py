import http

from flask import jsonify, make_response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from api.v1.utils.decorators import token_not_in_block_list, admin_permission
from db.db import sql_db
from models.db_models import Role


class RoleRemove(Resource):
    @jwt_required()
    @admin_permission()
    @token_not_in_block_list()
    def delete(self, role_id):
        """
        Method to delete the role
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
            description: Response after delete the role
            schema:
              properties:
                msg:
                  type: string
                  description: Response message
        """
        try:
            role = Role.query.filter_by(id=role_id).first()
            if not role:
                return make_response(
                    jsonify(msg=f"Role {role_id} not found"),
                    http.HTTPStatus.BAD_REQUEST,
                )
            sql_db.session.delete(role)
            sql_db.session.commit()
            return make_response(
                jsonify(msg=f"Role {role_id} removed"),
                http.HTTPStatus.OK,
            )
        except IntegrityError as error:
            sql_db.session.rollback()
            make_response(jsonify(msg=str(error)), http.HTTPStatus.BAD_REQUEST)
