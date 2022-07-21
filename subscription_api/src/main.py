from fastapi import FastAPI

from api.v1.subscriptions.views import router as subscription_router
from api.v1.transactions.views import router as transaction_router
from db.database import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(subscription_router, prefix="/api/billing/v1/subscriptions", tags=["subscriptions"])
app.include_router(transaction_router, prefix="/api/billing/v1/transactions", tags=["transactions"])
