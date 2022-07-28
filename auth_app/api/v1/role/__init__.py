from flask import Blueprint
from flask_restful import Api

role_bp = Blueprint('role', __name__, url_prefix='/api/auth/v1/role')
role_api = Api(role_bp)

from . import routes