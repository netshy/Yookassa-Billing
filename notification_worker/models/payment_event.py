from models.event import BaseEventEvent


class PaymentEvent(BaseEventEvent):
    user_id: str
