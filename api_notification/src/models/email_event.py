from typing import List

from models.choices import NotificationType
from models.event import BaseEventEvent
from orjson import orjson
from pydantic import BaseModel

from utils import orjson_dumps


class DataDetail(BaseModel):
    user_ids: List[str]
    film_ids: List[str]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class EmailEvent(BaseEventEvent):
    data: DataDetail
    subject: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class EmailNotificationBody(BaseModel):
    data: DataDetail
    subject: str
    template_id: str
    is_advertisement: bool
    type: NotificationType
