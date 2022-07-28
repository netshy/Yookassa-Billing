from enum import Enum


class CurrencyTypeEnum(str, Enum):
    USD = "USD"
    RUB = "RUB"


class SubscriptionPlanStatusEnum(str, Enum):
    Active = "active"
    Archived = "archived"


class SubscriptionStatus(str, Enum):
    Active = "active"
    Expired = "expired"
    Cancelled = "cancelled"


class TransactionStatus(str, Enum):
    Processing = "processing"
    Paid = "paid"
    Declined = "declined"


class RefundStatus(str, Enum):
    Processing = "processing"
    Approved = "approved"
    Declined = "declined"
