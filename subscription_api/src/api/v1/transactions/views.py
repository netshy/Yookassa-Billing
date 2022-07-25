from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request

from api.v1.transactions.messages import ALREADY_EXIST, PENDING_TRANSACTION
from db.service.pg_service import PostgresService, get_db_service
from schemas.subscription_schema import CreateSubscriptionSchema
from schemas.transaction import TransactionSchema, TransactionConfirmationUrl
from services.payment.yookass import YooKassPayment, get_payment_service

router = APIRouter()


@router.get("/", response_model=List[TransactionSchema])
def transactions_list(db_service: PostgresService = Depends(get_db_service)):
    transactions = db_service.get_all_transactions()
    return transactions


@router.post("/", response_model=TransactionConfirmationUrl)
def create_subscription(
        request: Request,
        data: CreateSubscriptionSchema,
        db_service: PostgresService = Depends(get_db_service),
        payment_service: YooKassPayment = Depends(get_payment_service)
):
    # check if user have active subscription
    is_exist = db_service.check_active_user_subscription(
        subscription_plan_id=data.subscription_plan_id,
        customer_id=request.user.id
    )
    if is_exist:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail=ALREADY_EXIST
        )
    # check if user have pending transaction
    is_pending = db_service.check_pending_transaction(
        customer_id=request.user.id
    )
    if is_pending:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail=PENDING_TRANSACTION
        )
    data = payment_service.create_payment(
        user_id=request.user.id,
        subscription_id=data.subscription_plan_id
    )
    return TransactionConfirmationUrl(confirmation_url=data)


@router.get("/{transaction_id}", response_model=TransactionSchema)
def transaction_get(transaction_id: str, db_service: PostgresService = Depends(get_db_service)):
    transaction = db_service.get_transaction_by_id(transaction_id)
    return transaction
