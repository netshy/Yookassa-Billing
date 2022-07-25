from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from starlette.middleware.authentication import AuthenticationMiddleware
from yookassa import Configuration

from api.v1.subscription_plans.views import router as subscription_plans_router
from api.v1.transactions.views import router as transaction_router
from core.auth.middleware import CustomAuthBackend
from db import storage
from db.database import Base, engine, SessionLocal
from settings import billing_setting

app = FastAPI(
    title=billing_setting.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

app.add_middleware(AuthenticationMiddleware, backend=CustomAuthBackend())
Configuration.configure(billing_setting.YOOKASSA_ID, billing_setting.YOOKASSA_SECRET)


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
    storage.db_storage = SessionLocal()


@app.on_event("shutdown")
async def shutdown():
    await storage.db_storage.close()


app.include_router(subscription_plans_router, prefix="/api/billing/v1/subscription_plans", tags=["subscription_plans"])
app.include_router(transaction_router, prefix="/api/billing/v1/transactions", tags=["transactions"])

