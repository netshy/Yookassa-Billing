from datetime import datetime

from pydantic import BaseModel


class BillingBase(BaseModel):
    id: str

    class Config:
        orm_mode = True


class DateTimeBase(BillingBase):
    create_at: datetime
    updated_at: datetime


class SubscriptionPlanSchema(BillingBase):

    price: int
    duration: int
    currency: str
    status: str


class TransactionSchema(BillingBase):
    customer_id: str
    plan_id: str
    session_id: str
    status: str
    code: str


class SubscriptionSchema(DateTimeBase):
    customer_id: str
    plan_id: str
    start_date: datetime
    end_date: datetime
    status: str


class RefundSchema(DateTimeBase):
    transaction_id: str
    customer_id: str
    amount: int
    status: str
