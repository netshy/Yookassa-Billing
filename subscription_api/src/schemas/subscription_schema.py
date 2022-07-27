from datetime import datetime
import uuid
from pydantic import BaseModel


class BillingBase(BaseModel):
    id: uuid.UUID

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

    class Config:
        orm_mode = True


class SubscriptionSchema(DateTimeBase):
    customer_id: uuid.UUID
    plan_id: uuid.UUID
    start_date: datetime
    end_date: datetime
    status: str
    payment_id: str

    class Config:
        orm_mode = True


class RefundSchema(DateTimeBase):
    transaction_id: uuid.UUID
    customer_id: uuid.UUID
    amount: int
    status: str

    class Config:
        orm_mode = True


class CreateSubscriptionSchema(BaseModel):
    subscription_plan_id: str
