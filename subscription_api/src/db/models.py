from db.database import Base
from db.enums import CurrencyTypeEnum, SubscriptionPlanStatusEnum, SubscriptionStatus, TransactionStatus, RefundStatus
from sqlalchemy import Column, Integer, String, Enum as enm, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from db.mixins import UUIDMixin, TimeStampedMixin, CustomerUUIDMixin


class SubscriptionPlanModel(UUIDMixin, Base):
    __tablename__ = "subscription_plan"

    name = Column(String)
    price = Column(Integer)
    duration = Column(Integer)
    currency = Column(enm(CurrencyTypeEnum))
    status = Column(enm(SubscriptionPlanStatusEnum))


class SubscriptionModel(UUIDMixin, TimeStampedMixin, CustomerUUIDMixin, Base):
    __tablename__ = "subscription"

    plan_id = Column(UUID, ForeignKey("subscription_plan.id"))
    start_date = Column(DateTime)
    status = Column(enm(SubscriptionStatus))


class TransactionModel(UUIDMixin, CustomerUUIDMixin, Base):
    __tablename__ = "transaction"
    
    plan_id = Column(UUID, ForeignKey("subscription_plan.id"))
    session_id = Column(String)
    code = Column(UUID)
    status = Column(enm(TransactionStatus))


class RefundModel(UUIDMixin, CustomerUUIDMixin, TimeStampedMixin, Base):
    __tablename__ = "refund"

    transaction_id = Column(UUID, ForeignKey("transaction.id"))
    amount = Column(Integer)
    status = Column(enm(RefundStatus))
    