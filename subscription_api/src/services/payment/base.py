from abc import ABC, abstractmethod
from typing import Optional


class PaymentBaseService(ABC):

    return_url: Optional[str] = None

    def __init__(self, storage_service=None, cache_storage=None):
        self.storage_service = storage_service
        self.cache_storage = cache_storage

    @abstractmethod
    def create_payment(self, *args, **kwargs):
        pass

    @abstractmethod
    def cancel_subscription(self, *args, **kwargs):
        pass
