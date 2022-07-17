import urllib.parse

from flask import redirect
from flask_restful import Resource

from .settings import YANDEX_OAUTH_URL, YANDEX_OAUTH_PARAMS


class YandexSocialLogin(Resource):
    def get(self):
        url = YANDEX_OAUTH_URL
        params = YANDEX_OAUTH_PARAMS

        url_redirect = url + urllib.parse.urlencode(params)

        return redirect(url_redirect)

