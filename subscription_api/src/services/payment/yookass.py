import json
import uuid

from fastapi import Depends
from yookassa import Payment, Refund
import datetime as dt
from db.redis import RedisStorage
from db.service.pg_service import PostgresService, get_db_service
from db.storage import get_cache_storage
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

    async def cancel_subscription(self, user_id: str, subscription_id) -> bool:
        subscription = self.storage_service.get_customer_subscription_by_id(user_id, subscription_id)
        # we refund money only if there is at least more than 10 days left unlit subscription end
        days_left = (subscription.end_date - dt.datetime.now(tz=dt.timezone.utc)).days
        if days_left < 10:
            return False

        subscription_plan = self.storage_service.get_subscription_plan(subscription.plan_id)
        payment_id = subscription.payment_id
        amount_to_refund = subscription_plan.price / days_left
        refund = Refund.create(
            {
                "amount": {
                    "value": amount_to_refund,
                    "currency": "RUB"
                },
                "payment_id": payment_id
            }
        )
        if refund.status == "succeeded":
            self.storage_service.close_subscription(subscription_id)
            return True
        return False


def get_payment_service(
        storage_service: PostgresService = Depends(get_db_service),
        cache_storage: RedisStorage = Depends(get_cache_storage)
) -> YooKassPayment:
    return YooKassPayment(storage_service, cache_storage)
