from sqlalchemy.orm import Session

from db.models import SubscriptionPlanModel


def get_subscriptions_plan(db: Session):
    return db.query(SubscriptionPlanModel).all()


def get_subscriptions_plan_by_id(db: Session, subscription_id: str):
    return db.query(SubscriptionPlanModel).filter(SubscriptionPlanModel.id == subscription_id).first()
