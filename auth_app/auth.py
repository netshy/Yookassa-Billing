from flasgger import Swagger
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from config import Config
from db.db import init_db
from marshm import ma
from urls import init_routes_v1

jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)
    jwt.init_app(app)
    ma.init_app(app)
    Api(app, prefix="/auth/api/v1")

    Swagger(app, template=SWAGGER_TEMPLATE)
    init_routes_v1(app)

    with app.app_context():
        from api.v1.utils.jwt_callbacks import (  # noqa
            user_lookup_callback,
        )  # noqa | load callback before first request start
        from management import create_super_user  # noqa

    return app


SWAGGER_TEMPLATE = {
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "scheme": "bearer",
            "BearerFormat": "JWT",
        }
    },
    "security": [{"BearerAuth": []}],
}
