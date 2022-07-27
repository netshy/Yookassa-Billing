from models.event import BaseEventEvent
from orjson import orjson

from utils import orjson_dumps


class HelloEvent(BaseEventEvent):
    user_id: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
