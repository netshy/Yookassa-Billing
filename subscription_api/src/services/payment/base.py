from abc import ABC, abstractmethod
from typing import Optional


class PaymentBaseService(ABC):

    return_url: Optional[str] = None

    def __init__(self, secret_key: str, account_id: Optional[str] = None, storage=None):
        self.secret_key = secret_key
        self.account_id = account_id
        self.storage = storage

    @abstractmethod
    def create_payment(self, *args, **kwargs):
        pass

    @abstractmethod
    def cancel_subscription(self, *args, **kwargs):
        pass
