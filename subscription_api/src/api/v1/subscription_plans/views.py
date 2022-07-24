from typing import List

from fastapi import Depends, APIRouter

from db.service.pg_service import PostgresService, get_db_service
from schemas.subscription_schema import SubscriptionPlanSchema

router = APIRouter()


@router.get("/", response_model=List[SubscriptionPlanSchema])
def subscription_plans_list(db_service: PostgresService = Depends(get_db_service)):
    subscription_plans = db_service.get_all_subscription_plans()
    return subscription_plans


@router.get("/{subscription_id}", response_model=SubscriptionPlanSchema)
def subscription_plan_get(subscription_id: str, db_service: PostgresService = Depends(get_db_service)):
    subscription_plan = db_service.get_subscriptions_plan_by_id(subscription_id)
    return subscription_plan
