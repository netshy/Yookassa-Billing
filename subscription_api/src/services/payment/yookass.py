import json
from typing import Tuple

from dateutil import parser
import uuid

from fastapi import Depends
from yookassa import Payment, Refund
import datetime as dt

from yookassa.domain.exceptions import BadRequestError

from db.redis import RedisStorage
from db.service.pg_service import PostgresService, get_db_service
from db.storage import get_cache_storage
from schemas.subscription_schema import RefundSchema
from schemas.transaction import PaymentTransactionSchema
from services.payment.base import PaymentBaseService


class YooKassPayment(PaymentBaseService):
    return_url: str = "http://127.0.0.1/api/billing/v1/yokas_success"

    async def create_payment(self, user_id: str, subscription_id: str) -> str:
        cache_data = await self.cache_storage.get(f"{user_id}_{subscription_id}")
        if cache_data:
            return cache_data
        plan = self.storage_service.get_subscription_plan(subscription_id)
        idempotence_key = str(uuid.uuid4())
        payment = Payment.create(
            {
                "amount": {
                    "value": float(plan.price),
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": "http://127.0.0.1"
                },
                "metadata": {"key": idempotence_key},
                "capture": True,
                "description": f"Оплата тарифного плана {plan.name}. Стоимость: {plan.price}{plan.currency}."
            }, idempotence_key
        )
        payment_data = json.loads(payment.json())
        amount = payment_data.pop("amount")
        transaction_data = PaymentTransactionSchema(
            **payment_data,
            customer_id=user_id,
            code=idempotence_key,
            plan_id=subscription_id,
            amount=float(amount["value"])
        )
        self.storage_service.create_transaction(transaction_data)
        await self.cache_storage.set(
            key=f"{user_id}_{subscription_id}",
            value=payment.confirmation.confirmation_url, expire=1200
        )
        return payment.confirmation.confirmation_url

    async def cancel_subscription(self, user_id: str, subscription_id: str) -> bool:
        subscription = self.storage_service.get_customer_subscription_by_id(user_id, subscription_id)
        # we refund money only if there is at least more than 10 days left unlit subscription end
        days_left = (subscription.end_date - dt.datetime.now(tz=dt.timezone.utc)).days
        if days_left < 10:
            return False

        subscription_plan = self.storage_service.get_subscription_plan(subscription.plan_id)
        payment_id = subscription.payment_id
        amount_to_refund = (subscription_plan.price/subscription_plan.duration)*days_left
        try:
            refund = Refund.create(
                {
                    "amount": {
                        "value": amount_to_refund,
                        "currency": "RUB"
                    },
                    "payment_id": payment_id
                }
            )
        except BadRequestError:
            return False
        formatted_refund = RefundSchema(
            id=refund.id,
            payment_id=refund.payment_id,
            customer_id=user_id,
            amount=float(refund.amount.value),
            status=refund.status,
            created_at=parser.parse(refund.created_at)
        )
        self.storage_service.create_refund(formatted_refund)
        if refund.status == "succeeded":
            self.storage_service.close_subscription(subscription_id)
            return True
        return False

    async def handle_callback(self, callback_data: dict) -> Tuple[str, bool]:
        types = {
            "payment.succeeded": "payment",
            "payment.canceled": "payment",
            "refund.succeeded": "refund"
        }
        event_type = callback_data["event"]
        data_object = callback_data["object"]
        return_type = types[event_type]

        if event_type == "payment.succeeded":
            transaction = self.storage_service.get_transaction_by_session_id(data_object["id"])
            self.storage_service.set_transaction_as_active(transaction.id)
            self.storage_service.create_user_subscription(transaction)
            return return_type, True
        elif event_type == "payment.canceled":
            self.storage_service.set_transaction_as_declined(data_object["id"])
            return return_type, False
        elif event_type == "refund.succeeded":
            self.storage_service.set_refund_as_succeeded(data_object["id"])
            self.storage_service.cancel_user_subscription_by_payment_id(data_object["payment_id"])
            return return_type, True


def get_payment_service(
        storage_service: PostgresService = Depends(get_db_service),
        cache_storage: RedisStorage = Depends(get_cache_storage)
) -> YooKassPayment:
    return YooKassPayment(storage_service, cache_storage)
