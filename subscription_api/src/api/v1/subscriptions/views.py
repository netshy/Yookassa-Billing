from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from db.crud import (
    get_all_subscription_plans,
    get_subscriptions_plan_by_id,
)
from db.database import get_db
from schemas.subscription_schema import SubscriptionPlanSchema

router = APIRouter()


@router.get("/", response_model=List[SubscriptionPlanSchema])
def subscription_plans_list(db: Session = Depends(get_db)):
    subscription_plans = get_all_subscription_plans(db)
    return subscription_plans


@router.get("/{subscription_id}", response_model=SubscriptionPlanSchema)
def subscription_plan_get(subscription_id: str, db: Session = Depends(get_db)):
    subscription_plan = get_subscriptions_plan_by_id(db, subscription_id)
    return subscription_plan
