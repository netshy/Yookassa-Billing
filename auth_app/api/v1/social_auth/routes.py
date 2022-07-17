from . import social_auth_api
from .callbacks import YandexSocialCallBack
from .login import YandexSocialLogin

social_auth_api.add_resource(YandexSocialLogin, "/yandex_login")
social_auth_api.add_resource(YandexSocialCallBack, "/yandex_callback")
