from aiohttp import ClientSession
from fastapi import Depends

from settings import billing_setting
from .http_client import get_http_client


class HttpService:
    def __init__(self, session: ClientSession):
        self.session = session

    async def send_user_payment_notification(self, customer_id: str, is_successful: bool, notification_type: str):
        notification_urls = {
            "refund": billing_setting.REFUND_NOTIFICATION_URL,
            "payment": billing_setting.PAYMENT_NOTIFICATION_URL
        }
        data = {"user_id": customer_id, "is_success": is_successful}
        url = notification_urls[notification_type]
        await self.session.post(url, json=data)


def get_http_service(
        http_session: ClientSession = Depends(get_http_client)
) -> HttpService:
    return HttpService(session=http_session)

