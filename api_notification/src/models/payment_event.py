from uuid import UUID

from orjson import orjson
from pydantic import BaseModel

from models.event import BaseEventEvent
from utils import orjson_dumps


class PaymentEvent(BaseEventEvent):
    user_id: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class UserPaymentNotification(BaseModel):
    user_id: UUID
    is_success: bool
