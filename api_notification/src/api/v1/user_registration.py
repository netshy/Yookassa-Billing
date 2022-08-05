import http
from uuid import UUID

from fastapi import APIRouter, HTTPException
from loguru import logger
from pika.exceptions import UnroutableError
from pydantic import BaseModel
from starlette.responses import Response

import broker
from api.config import config
from models.choices import NotificationType
from models.hello_event import HelloEvent

router = APIRouter()


class UserRegistration(BaseModel):
    user_id: UUID


@router.post("/user_registration", status_code=http.HTTPStatus.CREATED)
async def publish_hello_event_to_queue(request: UserRegistration):
    event = HelloEvent(
        is_advertisement=False,
        template_id=config.welcome_template_id,  # For new user we got 1 id template  # noqa
        user_id=str(request.user_id),
        type=NotificationType.welcome_email,
    )

    try:
        broker.rabbitmq_broker.basic_publish(event)
    except UnroutableError:
        logger.error("message was returned")
        raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND)
    except Exception as err:
        logger.error(f"publish error: {str(err)} | user_id: {request.user_id}")
        raise HTTPException(status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    return Response(status_code=201)
