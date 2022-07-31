from flask import Blueprint
from flask_restful import Api

role_bp = Blueprint("role", __name__, url_prefix="/auth/api/v1/role")
role_api = Api(role_bp)

from . import routes
