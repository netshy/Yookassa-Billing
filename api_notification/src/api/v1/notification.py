import http

from fastapi import APIRouter
from loguru import logger
from pika.exceptions import UnroutableError
from pydantic import BaseModel
from starlette.exceptions import HTTPException
from starlette.responses import Response

import broker
from api.config import config
from models.choices import NotificationType
from models.email_event import DataDetail, EmailEvent

router = APIRouter()


class EmailNotificationBody(BaseModel):
    data: DataDetail
    subject: str
    template_id: str
    is_advertisement: bool
    type: NotificationType


@router.post("/send_notification", status_code=http.HTTPStatus.CREATED)
async def send_notification_event(body: EmailNotificationBody):
    event = EmailEvent(
        data=body.data,
        is_advertisement=body.is_advertisement,
        template_id=body.template_id,
        type=body.type,
        subject=body.subject,
    )

    try:
        broker.rabbitmq_broker.channel.basic_publish(
            exchange=config.rabbit_exchange,
            routing_key=config.rabbit_email_events_queue,
            body=event.json(),
            mandatory=True,
        )
    except UnroutableError:
        logger.error("message was returned")
        raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND)
    except Exception as err:
        logger.error(f"publish error: {str(err)}")
        raise HTTPException(status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    return Response(status_code=201)
