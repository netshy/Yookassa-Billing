from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from api.v1.transactions.messages import ALREADY_EXIST, PENDING_TRANSACTION
from db.service.pg_service import PostgresService, get_db_service
from schemas.transaction import TransactionConfirmationUrl
from schemas.subscription_schema import CreateSubscriptionSchema
from services.payment.yookass import YooKassPayment, get_payment_service

router = APIRouter()


@router.post("/create", response_model=TransactionConfirmationUrl)
def create_subscription(
        data: CreateSubscriptionSchema,
        db_service: PostgresService = Depends(get_db_service),
        payment_service: YooKassPayment = Depends(get_payment_service)
):
    # check if user have active subscription
    is_exist = db_service.check_active_user_subscription(
        subscription_plan_id=data.subscription_plan_id,
        customer_id=data.customer_id
    )
    if is_exist:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail=ALREADY_EXIST
        )
    # check if user have pending transaction
    is_pending = db_service.check_pending_transaction(
        customer_id=data.customer_id
    )
    if is_pending:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail=PENDING_TRANSACTION
        )
    data = payment_service.create_payment(
        user_id=data.customer_id,
        subscription_id=data.subscription_plan_id
    )
    return TransactionConfirmationUrl(confirmation_url=data)