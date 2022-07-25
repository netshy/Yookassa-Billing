from fastapi import Depends

from db.database import SessionLocal
from db.models import SubscriptionPlanModel, TransactionModel, SubscriptionModel
from db.service.base import BaseDBService
from db.storage import get_db
from schemas.transaction import PaymentTransactionSchema


class PostgresService(BaseDBService):

    def get_all_subscription_plans(self):
        return self.session.query(SubscriptionPlanModel).all()

    def get_subscriptions_plan_by_id(self, subscription_id: str):
        return self.session.query(SubscriptionPlanModel).filter(SubscriptionPlanModel.id == subscription_id).first()

    def get_all_transactions(self):
        return self.session.query(TransactionModel).all()

    def get_transaction_by_id(self, transaction_id: str):
        return self.session.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()

    def check_active_user_subscription(self, subscription_plan_id: str, customer_id: str):
        return self.session.query(SubscriptionModel).filter(
            SubscriptionModel.customer_id == customer_id,
            SubscriptionModel.plan_id == subscription_plan_id,
            SubscriptionModel.status == "Active"
        ).first() is not None

    def check_pending_transaction(self, customer_id: str):
        return self.session.query(TransactionModel).filter(
            TransactionModel.customer_id == customer_id,
            TransactionModel.status == 'pending',
        ).first() is not None

    def get_subscription_plan(self, subscription_plan_id: str):
        return self.session.query(SubscriptionPlanModel).filter(
            SubscriptionPlanModel.id == subscription_plan_id
        ).first()

    def create_transaction(self, transaction_data: PaymentTransactionSchema):
        new_transaction = TransactionModel(
            **transaction_data.dict()
        )
        self.session.add(new_transaction)
        self.session.commit()


def get_db_service(
        session: SessionLocal = Depends(get_db),
) -> PostgresService:
    return PostgresService(session)
