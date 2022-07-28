from typing import Optional

from aiohttp import ClientSession

http_client_session: Optional[ClientSession] = None


def get_http_client() -> ClientSession:
    return http_client_session
