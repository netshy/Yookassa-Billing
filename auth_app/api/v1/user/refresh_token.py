import http

from flask import jsonify, make_response
from flask_jwt_extended import (
    get_jwt_identity,
    create_access_token,
    jwt_required,
)
from flask_restful import Resource

from api.v1.utils.decorators import refresh_token_in_redis_exists
from models import User


class UserRefreshToken(Resource):
    @jwt_required(refresh=True)
    @refresh_token_in_redis_exists()
    def post(self):
        """
        Method to refresh user access token
        ---
        tags:
          - user
        parameters:
          - in: header
            name: Authorization
            description: JWT refresh token
            default: "Bearer"
        responses:
          200:
            description: Response after user refresh it's token
            schema:
              properties:
                access_token:
                  type: string
                  description: Response message
        security:
          -
        """
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)

        if not user:
            return make_response(
                jsonify(msg="user not found"), http.HTTPStatus.NOT_FOUND
            )

        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token)
