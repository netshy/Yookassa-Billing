from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from config import Config
from db.postgres import install_models
from flasgger import Swagger

app = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

sql_db = SQLAlchemy(app)
install_models()
migrate = Migrate(app, sql_db)

api = Api(app, prefix="/api/auth/v1")
ma = Marshmallow(app)

SWAGGER_TEMPLATE = {
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "scheme": "bearer",
            "BearerFormat": "JWT"
        }
    },
    "security": [{"BearerAuth": []}]
}

swagger = Swagger(app, template=SWAGGER_TEMPLATE)

with app.app_context():
    from urls import init_routes_v1
    from api.v1.utils.jwt_callbacks import (
        user_lookup_callback,
    )  # noqa | load callback before first request start
    from management import create_super_user  # noqa

    init_routes_v1()
