from datetime import datetime
import uuid
from typing import Optional, Union

from pydantic import BaseModel


class BillingBase(BaseModel):
    id: uuid.UUID

    class Config:
        orm_mode = True


class DateTimeBase(BillingBase):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


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
    payment_id: str
    customer_id: Union[str, uuid.UUID]
    amount: int
    status: str

    class Config:
        orm_mode = True


class CreateSubscriptionSchema(BaseModel):
    subscription_plan_id: str
