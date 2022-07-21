from flask import Blueprint
from flask_restful import Api

social_auth_bp = Blueprint('social_auth', __name__, url_prefix='/api/auth/v1/social')
social_auth_api = Api(social_auth_bp)

from . import routes
