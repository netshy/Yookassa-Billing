from pydantic import BaseModel


class SubscriptionPlanSchema(BaseModel):
    id: str
    price: int
    duration: int
    currency: str
    status: str

    class Config:
        orm_mode = True
        