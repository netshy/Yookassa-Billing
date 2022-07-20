from enum import Enum


class CurrencyTypeEnum(str, Enum):
    USD = "USD"
    RUB = "RUB"


class SubscriptionPlanStatusEnum(str, Enum):
    Active = "Active"
    Archived = "Archived"


class SubscriptionStatus(str, Enum):
    Active = "Active"
    Expired = "Expired"


class TransactionStatus(str, Enum):
    Processing = "Processing"
    Pai = "Paid"
    Declined = "Declined"


class RefundStatus(str, Enum):
    Processing = "Processing"
    Approved = "Approved"
    Declined = "Declined"