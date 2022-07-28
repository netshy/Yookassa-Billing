from enum import Enum


class PaymentType(str, Enum):
    REFUND = "refund"
    PAYMENT = "payment"

    @classmethod
    def get_type(cls, payment_type: str):
        if payment_type == "refund":
            return cls.REFUND
        return cls.PAYMENT
