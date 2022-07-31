import logging

import grpc
import jwt
from fastapi.security import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from starlette.authentication import (
    AuthenticationBackend,
    AuthCredentials,
    UnauthenticatedUser,
)

from grcp_client.user_pb2 import UserRequest
from grcp_client.user_pb2_grpc import UserServiceStub
from settings import billing_setting
from .user import User

logger = logging.getLogger(__name__)
security = HTTPBearer()


class CustomAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        # Get JWT token from auth header
        authorization: str = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if scheme.lower() != "bearer":
            return AuthCredentials(), UnauthenticatedUser()

        if not credentials:
            return AuthCredentials(), UnauthenticatedUser()

        # Checks the validity of the JWT token, if token is invalid returns UnauthenticatedUser object
        try:
            jwt_decoded = jwt.decode(
                credentials,
                billing_setting.JWT_SECRET_KEY,
                algorithms=[billing_setting.JWT_ALGORITHM],
            )
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return AuthCredentials(), UnauthenticatedUser()

        with grpc.insecure_channel("flask_auth_web:50055") as channel:
            client = UserServiceStub(channel)
            request = UserRequest(login=jwt_decoded["login"])
            user = client.GetUser(request)

        auth_user = User(id=user.id, login=user.login, email=user.email)
        return AuthCredentials(["authenticated"]), auth_user
