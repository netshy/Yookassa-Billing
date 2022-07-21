from sqlalchemy.orm import Session

from db.models import SubscriptionPlanModel, TransactionModel


def get_all_subscription_plans(db: Session):
    return db.query(SubscriptionPlanModel).all()


def get_subscriptions_plan_by_id(db: Session, subscription_id: str):
    return db.query(SubscriptionPlanModel).filter(SubscriptionPlanModel.id == subscription_id).first()


def get_all_transactions(db: Session):
    return db.query(TransactionModel).all()


def get_transaction_by_id(db: Session, transaction_id: str):
    return db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
