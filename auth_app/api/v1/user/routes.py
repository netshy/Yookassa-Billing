from . import user_api
from .login import UserLogin
from .logout import UserLogout
from .refresh_token import UserRefreshToken
from .registration import UserRegistration
from .session import UserHistory
from .update_user_info import UserUpdateUsername, UserUpdatePassword

user_api.add_resource(UserRegistration, "/registration")
user_api.add_resource(UserLogin, "/login")
user_api.add_resource(UserLogout, "/logout")
user_api.add_resource(UserHistory, "/history")
user_api.add_resource(UserRefreshToken, "/token/refresh")
user_api.add_resource(UserUpdateUsername, "/username")
user_api.add_resource(UserUpdatePassword, "/password")
