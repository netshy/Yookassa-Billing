from fastapi import FastAPI
from loguru import logger

import broker
from api.v1 import user_registration, notification
from broker.rabbimq import PikaClient

app = FastAPI()


@app.on_event("startup")
def startup():
    # init queue
    broker.rabbitmq_broker = PikaClient()


@app.on_event("shutdown")
async def shutdown():
    broker.rabbitmq_broker.connection.close()
    logger.info("close rabbitmq connection")


app.include_router(user_registration.router, prefix="/notification/api/v1")
app.include_router(notification.router, prefix="/notification/api/v1")
