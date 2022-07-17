from environs import Env

env = Env()
env.read_env()

YANDEX_OAUTH_URL = "https://oauth.yandex.ru/authorize?"
YANDEX_OAUTH_PARAMS = {
    "response_type": "token",
    "client_id": "ff3a65476856490db595eb208a4984d5",
}
