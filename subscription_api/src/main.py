from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1.subscriptions.views import router as subscription_router
from api.v1.transactions.views import router as transaction_router
from db.database import Base, engine, SessionLocal
from settings import billing_setting
from db import storage


app = FastAPI(
    title=billing_setting.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
    storage.db_storage = SessionLocal()


@app.on_event("shutdown")
async def shutdown():
    await storage.db_storage.close()


app.include_router(subscription_router, prefix="/api/billing/v1/subscriptions", tags=["subscriptions"])
app.include_router(transaction_router, prefix="/api/billing/v1/transactions", tags=["transactions"])
