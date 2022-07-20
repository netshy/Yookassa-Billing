from sqlalchemy.orm import Session

from db.models import SubscriptionPlanModel


def get_subscriptions_plan(db: Session):
    return db.query(SubscriptionPlanModel).all()
