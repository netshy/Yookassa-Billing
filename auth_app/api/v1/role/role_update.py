import http

from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from api.v1.utils.decorators import token_not_in_block_list, admin_permission
from db.db import sql_db
from models.db_models import Role
from schemas.role import RoleUpdateSchema, SingleRoleSchema


class RoleUpdate(Resource):
    @jwt_required()
    @admin_permission()
    @token_not_in_block_list()
    def patch(self):
        """
        Method to update role properties
        ---
        tags:
          - role
        parameters:
          - in: body
            name: body
            schema:
              id: RoleUpdate
              required:
                - id
                - name
              properties:
                id:
                  type: string
                  description: Role PK.
                name:
                  type: string
                  description: Role type.
        responses:
          200:
            description: Response after update role properties
            schema:
              type: object
              properties:
                id:
                  type: string
                  description: PK role type
                role_type:
                  type: string
                  description: Name role type
        """
        try:
            data = RoleUpdateSchema().load(request.get_json())
            role = Role.query.filter_by(id=data["id"]).first()
            new_name = data["name"]
            if not role:
                return make_response(
                    jsonify(msg=f"Role {data['id']} not found"),
                    http.HTTPStatus.BAD_REQUEST,
                )
            role.role_type = new_name
            sql_db.session.add(role)
            sql_db.session.commit()
            return SingleRoleSchema.dump(role)
        except ValidationError as error:
            make_response(jsonify(msg=str(error)), http.HTTPStatus.BAD_REQUEST)
        except IntegrityError as error:
            sql_db.session.rollback()
            make_response(jsonify(msg=str(error)), http.HTTPStatus.BAD_REQUEST)
