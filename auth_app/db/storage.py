# Модуль для описания абстрактных классов работы с БД
from abc import ABC, abstractmethod


class BaseCacheStorage(ABC):
    def __init__(self, cache_engine):
        self.cache_engine = cache_engine

    @abstractmethod
    def get_token(self, key: str):
        pass

    @abstractmethod
    def set_token_to_black_list(self, key: str, value: str, expires: int):
        # when the user logout
        pass

    @abstractmethod
    def jti_token_in_black_list(self, key: str):
        pass

    @abstractmethod
    def close_connection(self):
        pass
