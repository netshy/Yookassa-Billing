import uuid
from datetime import datetime, timedelta

from fastapi import Depends

from db.database import SessionLocal
from db.enums import SubscriptionStatus, TransactionStatus
from db.models import SubscriptionPlanModel, TransactionModel, SubscriptionModel
from db.service.base import BaseDBService
from db.storage import get_db
from schemas.transaction import PaymentTransactionSchema


class PostgresService(BaseDBService):

    def get_all_subscription_plans(self):
        return self.session.query(SubscriptionPlanModel).all()

    def get_subscriptions_plan_by_id(self, subscription_id: str):
        return self.session.query(SubscriptionPlanModel).filter(SubscriptionPlanModel.id == subscription_id).first()

    def get_all_user_transactions(self, customer_id: str):
        return self.session.query(TransactionModel).filter(
            TransactionModel.customer_id == customer_id
        ).all()

    def get_user_transaction_by_id(self, transaction_id: str, customer_id: str):
        return self.session.query(TransactionModel).filter(
            TransactionModel.id == transaction_id,
            TransactionModel.customer_id == customer_id
        ).first()

    def get_transaction_by_session_id(self, session_id: str):
        return self.session.query(TransactionModel).filter(
            TransactionModel.session_id == session_id
        ).first()

    def get_customer_all_subscriptions(self, customer_id: str):
        return self.session.query(SubscriptionModel).filter(SubscriptionModel.customer_id == customer_id).all()

    def get_customer_subscription_by_id(self, customer_id: str, subscription_id: str):
        return self.session.query(SubscriptionModel).filter(
            SubscriptionModel.customer_id == customer_id,
            SubscriptionModel.id == subscription_id,
        ).first()

    def check_active_user_subscription_plan(self, subscription_plan_id: str, customer_id: str):
        return self.session.query(SubscriptionModel).filter(
            SubscriptionModel.customer_id == customer_id,
            SubscriptionModel.plan_id == subscription_plan_id,
            SubscriptionModel.status == "Active"
        ).first() is not None

    def check_active_user_subscription(self, subscription_id: str, customer_id: str):
        return self.session.query(SubscriptionModel).filter(
            SubscriptionModel.customer_id == customer_id,
            SubscriptionModel.id == subscription_id,
            SubscriptionModel.status == "Active"
        ).first() is not None

    def check_processing_transaction(self, customer_id: str):
        return self.session.query(TransactionModel).filter(
            TransactionModel.customer_id == customer_id,
            TransactionModel.status == TransactionStatus.Processing,
        ).first() is not None

    def get_subscription_plan(self, subscription_plan_id: str):
        return self.session.query(SubscriptionPlanModel).filter(
            SubscriptionPlanModel.id == subscription_plan_id
        ).first()

    def close_subscription(self, subscription_id: str):
        self.session.query(SubscriptionModel).filter(
            SubscriptionModel.id == subscription_id
        ).update({"status": "Cancelled"})
        self.session.commit()

    def create_transaction(self, transaction_data: PaymentTransactionSchema):
        new_transaction = TransactionModel(
            **transaction_data.dict()
        )
        self.session.add(new_transaction)
        self.session.commit()

    def set_transaction_as_active(self, transaction_id: str):
        self.session.query(TransactionModel).filter(
            TransactionModel.id == transaction_id
        ).update({"status": TransactionStatus.Paid, "paid": True})
        self.session.commit()

    def create_user_subscription(self, transaction: TransactionModel):
        plan: SubscriptionPlanModel = self.session.query(SubscriptionPlanModel).filter(
            SubscriptionPlanModel.id == transaction.plan_id
        ).first()
        end_date = datetime.now() + timedelta(days=plan.duration)
        new_user_subscription = SubscriptionModel(
            customer_id=transaction.customer_id,
            plan_id=transaction.plan_id,
            status=SubscriptionStatus.Active,
            payment_id=transaction.session_id,
            start_date=datetime.now(),
            end_date=end_date
        )
        self.session.add(new_user_subscription)
        self.session.commit()

def get_db_service(
        session: SessionLocal = Depends(get_db),
) -> PostgresService:
    return PostgresService(session)
