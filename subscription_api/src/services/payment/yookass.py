from fastapi import Depends

from db.storage import get_db
from services.payment.base import PaymentBaseService


class YooKassPayment(PaymentBaseService):
    return_url: str = "http://127.0.0.1/api/billing/v1/yokas_success"

    def create_payment(self, user_id: str, subscription_id: str):
        pass

    def cancel_subscription(self, user_id: str, subscription_id):
        pass


yookass_service = YooKassPayment(
    secret_key="123",
    account_id="321",
    storage=Depends(get_db)
)
