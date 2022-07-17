from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required
from flask_restful import Resource

from api.v1.utils.decorators import (
    refresh_token_in_redis_exists,
    token_not_in_block_list,
)
from db.redis import redis_cache_db


class UserLogout(Resource):
    @jwt_required()
    @refresh_token_in_redis_exists()
    @token_not_in_block_list()
    def delete(self):
        """
        Method to logout a user
        ---
        tags:
          - user
        responses:
          200:
            description: Response after logout
            schema:
              properties:
                msg:
                  type: string
                  description: Response message
        """
        jti = get_jwt()["jti"]
        redis_cache_db.set_token_to_black_list(jti, "")
        return jsonify(msg="access token revoked")
