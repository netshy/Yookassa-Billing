import http

from flask import request, make_response, jsonify
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from api.v1.utils.decorators import token_not_in_block_list
from auth import sql_db
from models.utils import hash_user_password
from schemas.user import UserUpdatePasswordSchema, UserUpdateUsernameSchema


class UserUpdatePassword(Resource):
    @jwt_required()
    @token_not_in_block_list()
    def patch(self):
        """
        Method to update users' password
        ---
        tags:
          - user
        parameters:
          - in: body
            name: body
            schema:
              id: UserUpdatePassword
              required:
                - password
              properties:
                password:
                  type: string
                  description: The user's new password.
        responses:
          200:
            description: Response after change user's password
            schema:
              properties:
                msg:
                  type: string
                  description: password was updated successfully
        """
        try:
            user_info = UserUpdatePasswordSchema().load(request.get_json())
        except ValidationError as err:
            return make_response(
                jsonify(msg=str(err)), http.HTTPStatus.BAD_REQUEST
            )

        if not current_user:
            return make_response(
                jsonify(msg="user not found"), http.HTTPStatus.NOT_FOUND
            )

        current_user.password = hash_user_password(user_info["password"])
        sql_db.session.commit()

        return make_response(
            jsonify(msg="password was updated successfully"),
            http.HTTPStatus.OK,
        )


class UserUpdateUsername(Resource):
    @jwt_required()
    @token_not_in_block_list()
    def patch(self):
        """
        Method to update users' username
        ---
        tags:
          - user
        parameters:
          - in: body
            name: body
            schema:
              id: UserUpdateUsername
              required:
                - username
              properties:
                username:
                  type: string
                  description: The user's new username.
        responses:
          200:
            description: Response after change user's password
            schema:
              properties:
                msg:
                  type: string
                  description: username was updated successfully
        """
        try:
            user_info = UserUpdateUsernameSchema().load(request.get_json())
        except ValidationError as err:
            return make_response(
                jsonify(msg=str(err)), http.HTTPStatus.BAD_REQUEST
            )

        if not current_user:
            return make_response(
                jsonify(msg="user not found"), http.HTTPStatus.NOT_FOUND
            )

        new_username = user_info["username"]

        if new_username == current_user.login:
            return make_response(
                jsonify(msg="username in request equal username in db"),
                http.HTTPStatus.NO_CONTENT,
            )

        try:
            current_user.login = new_username
            sql_db.session.commit()
        except IntegrityError:
            return make_response(
                jsonify(msg=f"login - {new_username}, already exists"),
                http.HTTPStatus.BAD_REQUEST,
            )

        return make_response(
            jsonify(msg="username was updated successfully!"),
            http.HTTPStatus.OK,
        )
