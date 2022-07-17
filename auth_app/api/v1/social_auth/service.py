import requests
import http

class YandexUserInfoService:
    AUTH_HEADERS = {"Authorization": "OAuth {access_token}"}
    USER_INFO_URL = "https://login.yandex.ru/info"

    def __init__(self, access_token):
        self._access_token = access_token

    def get_user_info(self):
        response = requests.get(self.USER_INFO_URL, headers=self.AUTH_HEADERS)
        if response.status_code == http.HTTPStatus.UNAUTHORIZED:
            pass
        if response.status_code == http.HTTPStatus.OK:
            user_data = response.json()





