from db.database import SessionLocal
from db.models import SubscriptionPlanModel, TransactionModel
from fastapi import Depends

from db.service.base import BaseDBService
from db.storage import get_db


class PostgresService(BaseDBService):

    def get_all_subscription_plans(self):
        return self.session.query(SubscriptionPlanModel).all()

    def get_subscriptions_plan_by_id(self, subscription_id: str):
        return self.session.query(SubscriptionPlanModel).filter(SubscriptionPlanModel.id == subscription_id).first()

    def get_all_transactions(self):
        return self.session.query(TransactionModel).all()

    def get_transaction_by_id(self, transaction_id: str):
        return self.session.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()


def get_db_service(
        session: SessionLocal = Depends(get_db),
) -> PostgresService:
    return PostgresService(session)
