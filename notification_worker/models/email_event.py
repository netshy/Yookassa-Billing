from typing import List

from pydantic import BaseModel

from models.event import BaseEventEvent


class DataDetail(BaseModel):
    user_ids: List[str]
    film_ids: List[str]


class EmailEvent(BaseEventEvent):
    data: DataDetail
    subject: str
