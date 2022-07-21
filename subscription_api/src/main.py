from typing import List

from fastapi import FastAPI, Depends
from db.database import Base, engine, SessionLocal
from schemas.subscription_schema import SubscriptionPlanSchema, TransactionSchema
from db.crud import (
    get_all_subscription_plans, get_subscriptions_plan_by_id, get_all_transactions,
    get_transaction_by_id,
)
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/billing/v1/hello")
async def root():
    return {"message": "Hello World"}


@app.get("/api/billing/v1/subscriptions", response_model=List[SubscriptionPlanSchema])
def get_subscription_plans(db: Session = Depends(get_db)):
    subscription_plans = get_all_subscription_plans(db)
    return subscription_plans


@app.get("/api/billing/v1/subscriptions/{subscription_id}", response_model=SubscriptionPlanSchema)
def get_subscription_plan(subscription_id: str, db: Session = Depends(get_db)):
    subscription_plan = get_subscriptions_plan_by_id(db, subscription_id)
    return subscription_plan


@app.get("/api/billing/v1/transactions", response_model=List[TransactionSchema])
def get_transactions(db: Session = Depends(get_db)):
    transactions = get_all_transactions(db)
    return transactions

@app.get("/api/billing/v1/transactions/{transaction_id}", response_model=TransactionSchema)
def get_transaction(transaction_id: str, db: Session = Depends(get_db)):
    transaction = get_transaction_by_id(db, transaction_id)
    return transaction