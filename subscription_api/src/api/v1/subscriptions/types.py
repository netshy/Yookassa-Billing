from enum import Enum


class PaymentType(str, Enum):
    REFUND = "refund"
    PAYMENT = "payment"
