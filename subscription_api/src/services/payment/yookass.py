import json
import uuid

from fastapi import Depends
from yookassa import Payment

from db.redis import RedisStorage
from db.service.pg_service import PostgresService, get_db_service
from db.storage import get_cache_storage
from schemas.transaction import PaymentTransactionSchema
from services.payment.base import PaymentBaseService


class YooKassPayment(PaymentBaseService):
    return_url: str = "http://127.0.0.1/api/billing/v1/yokas_success"

    def create_payment(self, user_id: str, subscription_id: str) -> str:
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
        return payment.confirmation.confirmation_url

    def cancel_subscription(self, user_id: str, subscription_id):
        pass


def get_payment_service(
        storage_service: PostgresService = Depends(get_db_service),
        cache_storage: RedisStorage = Depends(get_cache_storage)
) -> YooKassPayment:
    return YooKassPayment(storage_service, cache_storage)
