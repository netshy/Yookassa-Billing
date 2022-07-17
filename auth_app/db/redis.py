from redis import Redis

from config import Config
from db.storage import BaseCacheStorage


class RedisCache(BaseCacheStorage):
    def get_token(self, key: str) -> bytes:
        """Method return users token if exists in Redis."""
        return self.cache_engine.get(key)

    def set_refresh_token(self, key: str, value: str):
        """Set refresh token to cache.

        Parameters:
            key: str - expected input is user's session_id
            value: str - user's refresh jwt token
        """
        self.cache_engine.set(key, value)

    def set_token_to_black_list(
        self,
        key: str,
        value: str,
        expires: int = Config.JWT_ACCESS_TOKEN_EXPIRES,
    ):
        # when the user logout
        self.cache_engine.set(f"{key}_black_list", value, expires)

    def jti_token_in_black_list(self, key: str) -> bool:
        return self.cache_engine.get(f"{key}_black_list") is not None

    def close_connection(self):
        self.cache_engine.close()


redis_cache_db = RedisCache(
    Redis(
        host=Config.REDIS_HOST,
        port=Config.REDIS_PORT,
        password=Config.REDIS_PASSWORD,
    )
)
