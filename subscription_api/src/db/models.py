from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base
from db.mixins import UUIDMixin, TimeStampedMixin, CustomerUUIDMixin


class SubscriptionPlanModel(UUIDMixin, Base):
    __tablename__ = "subscription_plan"

    name = Column(String)
    price = Column(Integer)
    duration = Column(Integer)
    currency = Column(String)
    status = Column(String)


class SubscriptionModel(UUIDMixin, TimeStampedMixin, CustomerUUIDMixin, Base):
    __tablename__ = "subscription"

    plan_id = Column(UUID, ForeignKey("subscription_plan.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String)
    payment_id = Column(String)


class TransactionModel(UUIDMixin, CustomerUUIDMixin, TimeStampedMixin, Base):
    __tablename__ = "transaction"
    
    plan_id = Column(UUID, ForeignKey("subscription_plan.id"))
    session_id = Column(String)
    code = Column(String)
    status = Column(String)
    paid = Column(Boolean)
    description = Column(String)
    amount = Column(Integer)


class RefundModel(UUIDMixin, CustomerUUIDMixin, TimeStampedMixin, Base):
    __tablename__ = "refund"

    transaction_id = Column(UUID, ForeignKey("transaction.id"))
    amount = Column(Integer)
    status = Column(String)
