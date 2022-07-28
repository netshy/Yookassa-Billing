from models.event import BaseEventEvent


class HelloEvent(BaseEventEvent):
    user_id: str
