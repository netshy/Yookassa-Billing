from abc import ABC, abstractmethod

from db.database import SessionLocal


class BaseDBService(ABC):

    def __init__(self, session: SessionLocal):
        self.session = session

    @abstractmethod
    def get_all_subscription_plans(self):
        pass

    @abstractmethod
    def get_subscriptions_plan_by_id(self, subscription_id: str):
        pass

    @abstractmethod
    def get_all_user_transactions(self, customer_id: str):
        pass

    @abstractmethod
    def get_user_transaction_by_id(self, transaction_id: str, customer_id: str):
        pass
