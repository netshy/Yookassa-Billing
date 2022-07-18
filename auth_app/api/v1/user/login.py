import http

from flask import request, jsonify, make_response, Response
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource
from marshmallow import ValidationError

from auth import sql_db
from db.redis import redis_cache_db
from models import User, Session
from schemas.user import UserLoginSchema


class UserLogin(Resource):
    def post(self):
        """
        Method to login a user
        ---
        tags:
          - user
        parameters:
          - in: body
            name: body
            schema:
              id: UserLogin
              required:
                - username
                - password
              properties:
                username:
                  type: string
                  description: The user's username.
                password:
                  type: string
                  description: The user's password.
        responses:
          200:
            description: Response after creating new user
            schema:
              properties:
                access_token:
                  type: string
                  description: User access token
                refresh_token:
                  type: string
                  description: User refresh token
        """
        try:
            login_info = UserLoginSchema().load(request.json)
        except ValidationError as err:
            return Response(str(err), status=http.HTTPStatus.BAD_REQUEST)

        username = login_info["username"]
        password = login_info["password"]

        user = User.find_by_login(username)
        if user is None:
            return make_response(
                jsonify({"msg": "user not found"}), http.HTTPStatus.NOT_FOUND
            )
        is_password_valid = user.check_user_password(password)

        if not is_password_valid:
            return make_response(
                jsonify({"msg": "incorrect password"}),
                http.HTTPStatus.FORBIDDEN,
            )

        # adding a login entry
        session = Session.find_by_user_and_agent(
            user_id=user.id, user_agent=request.user_agent.string
        )
        if session is None:
            session = Session(
                user_id=user.id, user_agent=request.user_agent.string
            )
            sql_db.session.add(session)
        session.updated = sql_db.func.now()
        sql_db.session.commit()

        # create tokens with roles
        additional_claims = {
            "login": user.login,
            "roles": user.get_all_roles(),
            "session_id": str(session.id),
        }
        access_token = create_access_token(
            identity=user, additional_claims=additional_claims
        )
        refresh_token = create_refresh_token(
            identity=user,
            expires_delta=False,
            additional_claims=additional_claims,
        )
        redis_cache_db.set_refresh_token(str(session.id), refresh_token)

        return jsonify(
            access_token=access_token,
            refresh_token=refresh_token,
        )
