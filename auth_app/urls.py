from api.v1.role import role_bp
from api.v1.social_auth import social_auth_bp
from api.v1.user import user_bp


def init_routes_v1(app):
    app.register_blueprint(role_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(social_auth_bp)
