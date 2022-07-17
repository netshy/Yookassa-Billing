import http
from functools import wraps

from flask import make_response, jsonify
from flask_jwt_extended import get_jwt

from config import ADMIN_ROLE
from db.redis import redis_cache_db


def refresh_token_in_redis_exists():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            session_id = get_jwt()["session_id"]
            refresh_token = redis_cache_db.get_token(session_id)
            if refresh_token:
                return fn(*args, **kwargs)
            else:
                return make_response(
                    jsonify(msg="refresh token in redis not exists"),
                    http.HTTPStatus.FORBIDDEN,
                )

        return decorator

    return wrapper


def token_not_in_block_list():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            jti: str = get_jwt()["jti"]
            token_in_redis = redis_cache_db.jti_token_in_black_list(jti)
            if not token_in_redis:
                return fn(*args, **kwargs)
            else:
                return make_response(
                    jsonify(msg="access token was revoked"),
                    http.HTTPStatus.FORBIDDEN,
                )

        return decorator

    return wrapper


def admin_permission():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            jwt = get_jwt()
            if ADMIN_ROLE in jwt["roles"]:
                return fn(*args, **kwargs)
            else:
                return make_response(
                    jsonify(msg="Access denied. Only administrator allowed"),
                    http.HTTPStatus.FORBIDDEN,
                )

        return decorator

    return wrapper
