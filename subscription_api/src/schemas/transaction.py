from typing import Optional

from pydantic import BaseModel, Field


class CommonTransactionField(BaseModel):
    customer_id: str
    plan_id: str
    session_id: str
    status: str
    code: str
    description: Optional[str]
    paid: bool
    amount: float


class TransactionSchema(CommonTransactionField):
    id: str


class PaymentTransactionSchema(CommonTransactionField):
    session_id: str = Field(alias="id")

    class Config:
        allow_population_by_field_name = True


class TransactionConfirmationUrl(BaseModel):
    confirmation_url: str


class ConfirmationUrl(BaseModel):
    confirmation_url: str


class CreateTransactionSchema(BaseModel):
    customer_id: str
    subscription_plan_id: str
