from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request

from api.v1.subscriptions.types import PaymentType
from api.v1.transactions.messages import ALREADY_EXIST
from core.auth.wrapper import login_required
from db.service.pg_service import PostgresService, get_db_service
from services.http_service import HttpService, get_http_service
from schemas.subscription_schema import CreateSubscriptionSchema
from schemas.transaction import TransactionSchema, TransactionConfirmationUrl
from services.payment.yookass import YooKassPayment, get_payment_service

router = APIRouter()


@router.get("/", response_model=List[TransactionSchema])
@login_required()
async def transactions_list(
        request: Request,
        db_service: PostgresService = Depends(get_db_service)
):
    transactions = db_service.get_all_user_transactions(request.user.id)
    return transactions


@router.post("/", response_model=TransactionConfirmationUrl)
@login_required()
async def create_transaction(
        request: Request,
        data: CreateSubscriptionSchema,
        db_service: PostgresService = Depends(get_db_service),
        payment_service: YooKassPayment = Depends(get_payment_service),
):
    # check if user have active subscription
    is_exist = db_service.check_active_user_subscription_plan(
        subscription_plan_id=data.subscription_plan_id,
        customer_id=request.user.id
    )
    if is_exist:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail=ALREADY_EXIST
        )
    data = await payment_service.create_payment(
        user_id=request.user.id,
        subscription_id=data.subscription_plan_id
    )

    return TransactionConfirmationUrl(confirmation_url=data)


@router.post("/yookas_callback", status_code=HTTPStatus.OK)
async def yookas_callback(
        request: Request,
        payment_service: YooKassPayment = Depends(get_payment_service),
        http_service: HttpService = Depends(get_http_service)
):
    data = await request.json()
    payment_type, is_successful = await payment_service.handle_callback(data)
    # await http_service.send_user_payment_notification(
    #     customer_id=request.user.id,
    #     is_successful=is_successful,
    #     notification_type=PaymentType.get_type(payment_type).value
    # )


@router.get("/{transaction_id}", response_model=TransactionSchema)
@login_required()
async def transaction_get(
        transaction_id: str,
        request: Request,
        db_service: PostgresService = Depends(get_db_service)
):
    transaction = db_service.get_user_transaction_by_id(transaction_id, request.user.id)
    return transaction


