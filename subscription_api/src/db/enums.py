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
    Cancelled = "Cancelled"


class TransactionStatus(str, Enum):
    Pending = "pending"
    Paid = "paid"
    Declined = "declined"


class RefundStatus(str, Enum):
    Processing = "Processing"
    Approved = "Approved"
    Declined = "Declined"
