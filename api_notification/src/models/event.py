from orjson import orjson
from pydantic import BaseModel

from utils import orjson_dumps


class BaseEventEvent(BaseModel):
    is_advertisement: bool
    template_id: str
    type: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
