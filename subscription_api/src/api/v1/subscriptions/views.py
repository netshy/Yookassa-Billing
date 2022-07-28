from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request

from core.auth.wrapper import login_required
from db.service.pg_service import PostgresService, get_db_service
from schemas.subscription_schema import SubscriptionSchema
from services.http_service import HttpService, get_http_service
from services.payment.yookass import YooKassPayment, get_payment_service
from .messages import SUBSCRIPTION_NOT_EXIST, CANT_REFUND_SUBSCRIPTION
from .types import PaymentType

router = APIRouter()


@router.get("/", response_model=List[SubscriptionSchema])
@login_required()
def subscriptions_list(
        request: Request,
        db_service: PostgresService = Depends(get_db_service)
):
    subscriptions = db_service.get_customer_all_subscriptions(request.user.id)
    return subscriptions


@router.get("/{subscription_id}", response_model=SubscriptionSchema)
@login_required()
def get_subscription(
        subscription_id: str,
        request: Request,
        db_service: PostgresService = Depends(get_db_service)
):
    subscription = db_service.get_customer_subscription_by_id(request.user.id, subscription_id)
    return subscription


@router.delete("/{subscription_id}", status_code=HTTPStatus.NO_CONTENT)
@login_required()
async def cancel_subscription(
        subscription_id: str,
        request: Request,
        db_service: PostgresService = Depends(get_db_service),
        payment_service: YooKassPayment = Depends(get_payment_service),
        http_service: HttpService = Depends(get_http_service)
):
    subscription_is_exist = db_service.check_active_user_subscription(
        subscription_id=subscription_id,
        customer_id=request.user.id
    )
    if not subscription_is_exist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=SUBSCRIPTION_NOT_EXIST
        )

    response = await payment_service.cancel_subscription(
        user_id=request.user.id,
        subscription_id=subscription_id
    )
    if not response:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail=CANT_REFUND_SUBSCRIPTION
        )
    await http_service.send_user_payment_notification(
        customer_id=request.user.id,
        is_successful=True,
        notification_type=PaymentType.REFUND
    )

