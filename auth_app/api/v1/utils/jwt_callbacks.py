from typing import Optional

from auth import jwt
from models import User


@jwt.user_identity_loader
def user_identity_lookup(user: User) -> str:
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data) -> Optional[User]:
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()
