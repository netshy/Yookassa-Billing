from typing import List

from fastapi import FastAPI, Depends
from db.database import Base, engine, SessionLocal
from schemas.subscription_schema import SubscriptionPlanSchema
from db.crud import get_subscriptions_plan
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


@app.get("/api/subscription/v1/hello")
async def root():
    return {"message": "Hello World"}


@app.get("/api/subscription/v1/subscriptions", response_model=List[SubscriptionPlanSchema])
def get_subscription_plan(db: Session = Depends(get_db)):
    subscription_plans = get_subscriptions_plan(db)
    return subscription_plans
