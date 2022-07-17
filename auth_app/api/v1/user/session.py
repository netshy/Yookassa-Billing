from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource

from api.v1.utils.decorators import token_not_in_block_list
from models import Session
from schemas.session import MultipleSessionSchema


class UserHistory(Resource):
    @jwt_required()
    @token_not_in_block_list()
    def get(self) -> MultipleSessionSchema:
        """
        Method to list all user's sessions
        ---
        tags:
          - user
        responses:
          200:
            description: Response after creating new user
            schema:
               properties:
                 sessions:
                   type: object
                   properties:
                     id:
                       type: string
                     user_id:
                       type: string
                     user_agent:
                       type: string
                     created:
                       type: string
                     updated:
                       type: string
        """
        sessions = Session.query.filter_by(user_id=current_user.id)
        result = {"sessions": MultipleSessionSchema.dump(sessions)}
        return result
