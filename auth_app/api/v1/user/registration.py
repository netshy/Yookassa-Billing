import http

from flask import request, jsonify, make_response
from flask_restful import Resource
from marshmallow import ValidationError

from db.db import sql_db
from models.db_models import User
from schemas.user import UserRegistrationSchema


class UserRegistration(Resource):
    def post(self):
        """
        Method to register new user
        ---
        tags:
          - user
        parameters:
          - in: body
            name: body
            schema:
              id: UserRegistration
              required:
                - username
                - password
                - password_confirm
              properties:
                username:
                  type: string
                  description: The user's username.
                password:
                  type: string
                  description: The user's password.
                password_confirmation:
                  type: string
                  description: Password confirmation
        responses:
          201:
            description: Response after creating new user
            schema:
              properties:
                msg:
                  type: string
                  description: Response message
        """
        try:
            user = UserRegistrationSchema().load(request.get_json())
        except ValidationError as err:
            return make_response(
                jsonify({"msg": str(err)}),
                http.HTTPStatus.BAD_REQUEST,
            )

        if user["password"] != user["password_confirmation"]:
            return make_response(
                jsonify(
                    {
                        "msg": "Password and password confirmation should be equal"
                    }
                ),
                http.HTTPStatus.BAD_REQUEST,
            )

        # check if user already exist
        user_is_exist = User.find_by_login(user["username"])

        if user_is_exist:
            return make_response(
                jsonify({"msg": f"User {user['username']} already exists!"}),
                http.HTTPStatus.BAD_REQUEST,
            )

        email_is_exists = User.find_by_email(user["email"])
        if email_is_exists:
            return make_response(
                jsonify({"msg": f"User with email {user['email']} already exists!"}),
                http.HTTPStatus.BAD_REQUEST,
            )

        new_user = User(login=user["username"], password=user["password"], email=user["email"])
        sql_db.session.add(new_user)
        sql_db.session.commit()

        return make_response(
            jsonify({"msg": "user created"}),
            http.HTTPStatus.CREATED,
        )
